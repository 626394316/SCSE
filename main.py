import json
import re
import os
import requests
import arxiv
import random
import whisper
import cv2
import numpy as np
import time
import uuid
import edge_tts
import yaml

from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.output_parsers import JsonOutputParser
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.graphs import Neo4jGraph

from BCEmbedding import RerankerModel
from datetime import datetime
from operator import itemgetter
from bs4 import BeautifulSoup

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

import yaml
from graph_search import get_knowledge_graph

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # *：代表所有客户端
    allow_credentials=True,
    allow_methods=["GET,POST"],
    allow_headers=["*"],
)

with open("config.yml", 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

openai_api_base = "http://localhost:8000/v1"
openai_api_key = "none"

llm = ChatOpenAI(
    model_name=configs['llm_name'],
    openai_api_base=configs['llm_api_path'],
    openai_api_key="none",
    streaming=True,
    model_kwargs={
        "stop": ["Observation:", "Observation:\n"]
    },
    temperature=0
)

emo_llm = ChatOpenAI(
    model_name=configs['emo_llm_name'],
    openai_api_base=configs['emo_llm_api_path'],
    openai_api_key="none",
    streaming=True,
)

graph = Neo4jGraph(
    url=configs['neo4j_url'],
    username=configs['neo4j_username'],
    password=configs['neo4j_password'],
    database=configs['neo4j_database']
)

source = []

class Chatbot:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=configs['embedding_model_path'])
        self.vectorstore = FAISS.load_local("./vector_db/common_data", self.embeddings,
                                            allow_dangerous_deserialization=True)

        self.pr_vectorstore = FAISS.load_local("./vector_db/pr_data", self.embeddings,
                                               allow_dangerous_deserialization=True)
        self.RerankerModel = RerankerModel(model_name_or_path=configs['rerank_model_path'])

    def get_response(self, question):
        global source
        source = []
        is_stream = ""
        img_text_prompt = f"""
        你扮演文本分类的工具助手,类别有3种;
        如果文本是关于检索图片或者生成图片的,你返回1;
        如果文本是关于生成代码的,你返回2;
        如果文本是其他相关的，你返回3;

        以下是一些例子：
        例子1：'帮我生成一张华侨大学的照片',文本分类结果是1
        例子2:'帮我生成一张小狗的图片',文本分类结果是1
        例子3：'帮我生成一段快速排序的代码',文本分类结果是2
        例子4：'帮我生成一段哈希排序的代码',文本分类结果是2
        例子3：'学校图书馆怎么上网',文本分类结果是3
        例子4：'介绍一下你自己',文本分类结果是3
        请参考上面例子，直接给出一种分类结果，不要解释，不要多余的内容，不要多余的符号，不要多余的空格，不要多余的空行，不要多余的换行，不要多余的标点符号，不要多余的括号。
        请你对以下内容进行文本分类：
        {question}

        """
        img_or_text = llm.predict(img_text_prompt)
        print("img_or_text", img_or_text)
        if img_or_text == '1':
            source = []
            p_r = build_planning_prompt(question)
            for i in range(0, 8):
                res = get_res(p_r)
                print("res", res)
                if res.find("Action Input:") != -1:
                    args = get_args(res)
                    t_run = tool_chain(args)
                    p_r = p_r + res + "\nObservation: " + str(t_run.invoke(args)) + "\n"
                else:
                    p_r = p_r + res
                    p_r = p_r.split("Final Answer:")[-1]
                    break
            is_stream, llm_res = get_same_response(p_r)
            return is_stream, llm_res
        elif img_or_text == '2':
            source = []
            llm_res = llm.stream(question)
            return 1, llm_res
        elif img_or_text == '3':
            docs = self.vectorstore.similarity_search(query=question, k=1)
            passages = []
            for doc in docs:
                passages.append(doc.page_content)
            rerank_results = self.RerankerModel.rerank(query=question, passages=passages)
            print(rerank_results["rerank_scores"][0])
            if rerank_results["rerank_scores"][0] > 0.5:
                for doc in docs:
                    source.append({
                        'link': doc.metadata['source'],
                        'title': doc.metadata['source'].split('static/')[1].split('/')[1]
                    })
                print("source", source)
                prompt = f"""
                  你是华侨大学开发的AI助手,请你根据下列知识库的内容来回答问题,
                  如果无法从中得到答案,请说"抱歉，我暂时不知道如何解答该问题"即可,不允许在答案中添加编造成分和多余内容

                  以下是知识库:
                  {rerank_results["rerank_passages"][0]}
                  以上是知识库;

                  用户问题:
                  {question}
                  """
                llm_res = llm.stream(prompt)
            else:
                source = []
                p_r = build_planning_prompt(question)
                for i in range(0, 8):
                    res = get_res(p_r)
                    print("res", res)
                    if res.find("Action Input:") != -1:
                        args = get_args(res)
                        t_run = tool_chain(args)
                        p_r = p_r + res + "\nObservation: " + str(t_run.invoke(args)) + "\n"
                    else:
                        p_r = p_r + res
                        p_r = p_r.split("Final Answer:")[-1]
                        break
                is_stream, llm_res = get_same_response(p_r)

            return is_stream, llm_res

    def get_hqu_img(self, question):
        if "风景" in question:
            image_path = "/web_demo/src/assets/llm_img/华侨大学风景照.jpg"
        elif "夜景" in question:
            image_path = "/web_demo/src/assets/llm_img/华侨大学夜景.jpg"
        elif "图书馆" in question:
            image_path = "/web_demo/src/assets/llm_img/华侨大学图书馆.jpg"
        elif "logo" in question:
            image_path = "/web_demo/src/assets/llm_img/华侨大学logo.jpg"
        else:
            image_path = "/web_demo/src/assets/llm_img/华侨大学other.jpg"
        return image_path

    # 得到模式识别课程的回答
    def get_pr_exam_response(self, question):
        global source
        source = []
        graph_result = get_knowledge_graph(question, llm, graph)
        docs = self.pr_vectorstore.similarity_search(query=question, k=1)
        passages = []
        for doc in docs:
            passages.append(doc.page_content)
            source.append({
                'link': doc.metadata['source'],
                'title': doc.metadata['source'].split('static/')[1].split('/')[1]
            })
        print("source", source)
        print("graph_result", graph_result)
        # pr_vectorstore
        prompt = f"""
                You are a helpful question-answering agent. Your task is to analyze 
        and synthesize information from two sources: the top result from a similarity search 
        (unstructured information) and relevant data from a graph database (structured information). 
        Given the user's query: {question}, provide a meaningful and efficient answer in chinese based 
        on the insights derived from the following data:

        Unstructured information: {docs[0].page_content}. 
        Structured information: {graph_result}.

        note:Answer the question by referring only to two sources and adding nothing extra.
        note:If the two sources information contains latex formula,please return to the announcement intact.
        It is very important!
        """
        # print("prompt", prompt)
        result = llm.stream(prompt)
        print("result", result)
        return result

    def get_Emo_response(self, user_input):
        prompt = f"""
        现在你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的小V专家,
        用户有一些心理问题, 请你一步步诱导病人说出自己的问题进而提供解决问题的可行方案。
        如果你回复的好，我会给你一定的赏金。
        用户问题：{user_input}
        """
        print("Emo", prompt)
        result = emo_llm.stream(prompt)
        return result


# 返回流式输出的回答
def get_same_response(answer):
    if (".jpg" in answer):
        pattern = r'/web_demo.*?\.jpg'
        matches = re.findall(pattern, answer, re.IGNORECASE)
        if matches and matches[0] in answer:
            return 0, matches[0]
    else:
        prompt = f"""
        你只需要原封不动的返回答案的内容即可，一个字也不要修改，也不要添加任何多余的内容，这对我十分重要。
        以下是答案：
        {answer}
        以上是答案;
        """

        result = llm.stream(prompt)
        return 1, result


# 返回大模型的自我介绍
def self_qa():
    result_list = [
        "你好😊，我是华侨大学开发的校园AI助手小H，我旨在为学生和老师提供更便捷、高效的服务。",
        "你好😊，我是华侨大学精心打造的校园AI助手小H，我的目标是为校园中的大家提供更加智能、个性化的服务体验。",
        "你好😊，我是华侨大学精心孕育的校园AI助手小H，我在这里，就是为了给校园生活带来一抹智能的色彩，让学习、工作变得更加轻松愉快。",
        "你好😊，我是华侨大学倾力打造的校园AI助手小H，我的存在，就是为了让你在校园中的每一天都更加精彩，无论是学术探讨还是日常生活，我都将是你贴心的智能伙伴。"
    ]
    result = random.choices(result_list)
    return result


# 文本分类
def query_classify(question):
    prompt = f"""
    你扮演文本分类的工具助手,类别有2种;
    如果文本是关于要求介绍一下你自己的或者问候你的,你返回1;
    如果文本是其他相关的，你返回2;
    以下是一些例子：
    例子1：'你好',文本分类结果是1
    例子2:'介绍一下你自己',文本分类结果是1
    例子3：'你是谁',文本分类结果是1
    例子4：'介绍一下三国演义',文本分类结果是2
    例子4：'今天天气怎么样',文本分类结果是2
    例子4：'介绍一下华侨大学',文本分类结果是2
    请参考上面例子，直接给出一种分类结果，不要解释，不要多余的内容，不要多余的符号，不要多余的空格，不要多余的空行，不要多余的换行，不要多余的标点符号，不要多余的括号。
    请你对以下内容进行文本分类：
    {question}
    """
    result = llm.predict(prompt)
    return result


bot = Chatbot()


# 定义工具
@tool
def get_date() -> str:
    "通过这个工具可以获取今天的日期"
    time = datetime.now().date().strftime('%Y-%m-%d')
    return time

@tool
def arxiv_search(question: str):
    "当用户需要通过arxiv搜索引擎查询指定关键词的相关论文或文章资料时，可以调用这个工具"
    results = arxiv.Search(
        query=question[:300],
        max_results=1
    ).results()
    docs = [
        f'发表日期: {result.updated.date()}\n标题: {result.title}\n'
        f'作者: {", ".join(a.name for a in result.authors)}\n'
        f'文章摘要: {result.summary}'
        for result in results
    ]
    print("docs", docs)
    return docs


@tool
def make_img(question: str):
    "当用户需要根据关键词生成图片的时候,可以使用这个工具"
    # styles_option = [
    #     'dongman',  # 动漫
    #     'guofeng',  # 国风
    #     'xieshi',   # 写实
    #     'youhua',   # 油画
    #     'manghe',   # 盲盒
    # ]
    # aspect_ratio_options = [
    #     '16:9', '4:3', '3:2', '1:1',
    #     '2:3', '3:4', '9:16'
    # ]
    if ("华侨大学" in question):
        output_path = bot.get_hqu_img(question)
        print("output_path", output_path)
        return output_path
    else:
        response = requests.post(
            url='https://magicmaker.openxlab.org.cn/gw/edit-anything/api/v1/bff/sd/generate',
            data=json.dumps({
                "official": True,
                "prompt": question,
                "style": "xieshi",
                "poseT": False,
                "aspectRatio": "4:3"
            }),
            headers={'content-type': 'application/json'}
        )
        image_url = response.json()['data']['imgUrl']
        image_response = requests.get(image_url)
        image = cv2.imdecode(np.frombuffer(image_response.content, np.uint8), cv2.IMREAD_COLOR)

        # tmp_dir = os.path.join("./img", 'tmp_dir')
        tmp_dir = "./web_demo/src/assets/llm_img"
        os.makedirs(tmp_dir, exist_ok=True)
        timestamp = int(time.time() * 1000)
        unique_id = uuid.uuid4().int
        unique_number = f"{timestamp}{unique_id}"
        output_path = os.path.join(tmp_dir, f"{unique_number}.jpg").replace("\\", "/")
        print("output_path", output_path)
        # 保存输出
        cv2.imwrite(output_path, image)
        return output_path


@tool
def baidu_search(keyword: str) -> str:
    "通过搜索引擎查询指定关键词的相关资料"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.baidu.com",
        # 需要更换Cookie
        "Cookie": "BIDUPSID=4EA09413AA348579EBC32BB4171DA6C4; PSTM=1685953325; BAIDUID=4EA09413AA34857921D22606F3465DE3:SL=0:NR=20:FG=1; BD_UPN=12314753; MCITY=-%3A; BDUSS=d4V1kzMVE5TC02V0dzSzBHR0pPZzZjY2xXZ05-YkxPSlFYOTlqVWtlekUxVjFtSVFBQUFBJCQAAAAAAAAAAAEAAAA3oAABd2FuZ3BlbmdlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRINmbESDZmRX; BDUSS_BFESS=d4V1kzMVE5TC02V0dzSzBHR0pPZzZjY2xXZ05-YkxPSlFYOTlqVWtlekUxVjFtSVFBQUFBJCQAAAAAAAAAAAEAAAA3oAABd2FuZ3BlbmdlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRINmbESDZmRX; H_PS_PSSID=60269_60278_60282_60287_60296_60253; H_WISE_SIDS=60269_60278_60282_60287_60296_60253; H_WISE_SIDS_BFESS=60269_60278_60282_60287_60296_60253; BAIDUID_BFESS=4EA09413AA34857921D22606F3465DE3:SL=0:NR=20:FG=1; BD_CK_SAM=1; PSINO=3; delPer=0; BA_HECTOR=810l01ak80aha1a101ah0401evoeh21j58flh1v; ZFY=65gS58gkPrLw3aFizT:BRHNeW:AN:A3yhdtUx81zQ4:Aky8:C; shifen[389215454364_77942]=1716797107; BCLID=8729107127908649389; BCLID_BFESS=8729107127908649389; BDSFRCVID=43DOJeC62iPknV7toafpMW8kd_IPxeRTH6ao8FEfGw7FPXyfJA7mEG0P2U8g0KuM8DJTogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; BDSFRCVID_BFESS=43DOJeC62iPknV7toafpMW8kd_IPxeRTH6ao8FEfGw7FPXyfJA7mEG0P2U8g0KuM8DJTogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=JnIJoD8hJIK3fP36qRojh-40b2T22jnOM6T9aJ5nJDonDtTJKPbMQftXy4cUqPnbQjQkW-tbQpP-HJ7y3R6xytKN2h6waTcQBm6QKl0MLpQWbb0xyUQY3jDzbxnMBMni52OnapTn3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDFRj5-hDTjyDaR-htRX54ofW-oofK-5sh7_bf--D4FrMUTptb3yKCcj2x0y2bbrOfJ9bq5xy5K_hN7l045xbbvlbUnX5qcNMn6HQT3mDlQbbN3i-xuO3gQnWb3cWhvJ8UbSyfbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JD-50exbH55uHtRktVx5; H_BDCLCKID_SF_BFESS=JnIJoD8hJIK3fP36qRojh-40b2T22jnOM6T9aJ5nJDonDtTJKPbMQftXy4cUqPnbQjQkW-tbQpP-HJ7y3R6xytKN2h6waTcQBm6QKl0MLpQWbb0xyUQY3jDzbxnMBMni52OnapTn3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDFRj5-hDTjyDaR-htRX54ofW-oofK-5sh7_bf--D4FrMUTptb3yKCcj2x0y2bbrOfJ9bq5xy5K_hN7l045xbbvlbUnX5qcNMn6HQT3mDlQbbN3i-xuO3gQnWb3cWhvJ8UbSyfbPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JD-50exbH55uHtRktVx5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; B64_BOT=1; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=7da2HdXe6gMkTCYHhNWjWjBKf%2F91xi1Bc2ju7gIhGU8jSNH4YjL1%2BaTa6lI; baikeVisitId=c252a4ed-daf5-4079-8ca6-d287e0ffca21; COOKIE_SESSION=454_1_5_9_12_17_1_0_3_7_0_4_76645_0_0_0_1716797758_1716797108_1716799282%7C9%23409189_19_1716797105%7C9; BDSVRTM=34"
    }
    url = "https://www.baidu.com/s?wd=" + keyword
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    text = ""
    for i in soup.find_all("div", class_="result c-container xpath-log new-pmd"):
        try:
            text = text + "tite:" + i.find("a").text + "\n"
            text = text + "content:" + i.find("span", class_="content-right_2s-H4").text + "\n"
        except:
            continue
    return text


@tool
def takeout():
    "当用户想要点外卖的时候，可以调用这个工具"
    foods = [
        {"name": "宫保鸡丁饭", "price": 15.00},
        {"name": "鱼香肉丝饭", "price": 14.00},
        {"name": "叉烧饭", "price": 20.00},
        {"name": "牛肉拉面", "price": 16.00},
        {"name": "水饺", "price": 12.00}
    ]
    selected_food = random.choice(foods)
    result = f"已经为您点了{selected_food['name']},价格为{selected_food['price']}元,已自动从您学生卡支付"
    return result


@tool
def library() -> str:
    "当用户想要预定图书馆座位的时候可以使用这个工具"
    # 随机选择楼层
    floor = random.randint(1, 5)
    # 随机选择座位号
    seat_number = random.randint(1, 99)
    seat = f"{floor}-{seat_number}"
    result = f"已经为您检索到了空闲座位，预定了{seat}号座位，请及时前往就坐"
    return result


tool_list = [get_date, baidu_search, arxiv_search, make_img, library, takeout]


def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tool_list}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool


new_tool_list = [convert_to_openai_tool(i) for i in tool_list]

TOOL_DESC = """
{tool_name}: 工具描述:{tool_description} parameters: {tool_parameters} Format the arguments as a JSON object.
"""

REACT_PROMPT = """
You are an assistant who is good at calling external tools. 
Try your best to answer the following questions in Chinese. 
The tools you can use include:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}
Thought:
"""


def build_planning_prompt(query):
    tool_descs = []
    tool_names = []
    for tools in new_tool_list:
        tool_descs.append(
            TOOL_DESC.format(
                tool_name=tools["function"]["name"],
                tool_description=tools["function"]["description"],
                tool_parameters=json.dumps(
                    tools["function"]["parameters"], ensure_ascii=False
                )
            )
        )
        tool_names.append(tools["function"]["name"])
    tool_descs = '\n\n'.join(tool_descs)
    tool_names = ','.join(tool_names)
    prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names, query=query)
    return prompt


def get_res(prompt):
    response = llm.predict(prompt)
    return response


parser = JsonOutputParser()


def get_args(res):
    args0 = res.split("\nAction: ")[1].split("\nAction Input:")
    return {"name": args0[0], "arguments": parser.parse(args0[1])}


class Content(BaseModel):
    content: str


@app.post("/send_question")
async def send_question(content: Content):
    global source
    source = []
    question = content.content
    fl_res = query_classify(question)
    print("fl_res", fl_res)
    if fl_res == '1':
        _, result = get_same_response(self_qa())

        def generate():
            for text in result:
                yield str(text.content)

        return StreamingResponse(generate(), media_type="text/event-stream")
    else:
        is_stream, result = bot.get_response(question)
        print("is_stream", is_stream)
        if is_stream == 0:
            print('result', result.replace('"', ''))
            return result
        else:
            def generate():
                for text in result:
                    yield str(text.content)

            return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/send_exam_question")
async def send_exam_question(content: Content):
    question = content.content
    answer = bot.get_pr_exam_response(question)

    def add_spaces_to_brackets(text):
        # 正则表达式匹配连续的花括号
        pattern = r'(\{|\})+'
        # replaced_text = re.sub(r'\\(right|left)', r'\\lvert', text)
        # 使用re.sub函数替换匹配的连续花括号，在它们之间添加空格
        result = re.sub(pattern, lambda m: ' '.join(m.group()), text)
        return result

    # return answer
    def generate():
        for text in answer:
            text.content = add_spaces_to_brackets(text.content)
            print(text.content)
            yield str(text.content)

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/whisper")
async def to_whisper(file: UploadFile = File(...)):
    filename = file.filename
    file_content = await file.read()
    with open(f"./{filename}", "wb") as f:
        f.write(file_content)
    model = whisper.load_model("small")
    audio = whisper.load_audio(f"./{filename}")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions(prompt="以下是普通话的句子")
    result = whisper.decode(model, mel, options)
    print(result.text)
    return result.text


# 得到问题来源的接口
@app.post("/get_source")
async def get_source():
    global source
    source = source[-3:]
    return source


class Summarize(BaseModel):
    question: str
    answer: str


# 总结的接口
@app.post("/summarize")
async def llmSummarize(summarize: Summarize):
    question = summarize.question
    answer = summarize.answer
    # print(question,answer)
    prompt = f"""
    你的任务是，根据问题和答案，生成一个能够概括该对话的标题，
    这对我来说十分重要。
    如果你做的好，我会给你一定的赏金。
    问题:{question},
    答案:{answer},
    你概括的标题:
    """
    result = llm.predict(prompt)
    # print(result)
    return result


class ToTTS(BaseModel):
    content: str


@app.post("/tts")
async def tts(data: ToTTS):
    TEXT = data.content
    VOICE = "zh-CN-XiaoxiaoNeural"
    OUTPUT_FILE = "./test.mp3"
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    return FileResponse(OUTPUT_FILE, media_type="audio/mpeg")


@app.post("/send_emo_question")
async def send_emo_question(content: Content):
    question = content.content
    answer = bot.get_Emo_response(question)

    def generate():
        for text in answer:
            yield str(text.content)

    return StreamingResponse(generate(), media_type="text/event-stream")

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=7070, reload=True)
# uvicorn main:app --host 127.0.0.1 --port 7091 --workers 1 --reload
