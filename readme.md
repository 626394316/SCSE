## SCSE 智慧校园的超级入口

<div align=center><img src="/assets/logo.png"></div>

### 📖 项目介绍

　　目前各大高校领域将各种信息分布在不同的部门信息门户下，存在典型的信息孤岛问题，各个部门信息没有形成互通。当前，老师和学生存在很多有关本校相关文件、政策和活动等众多方面智能问答的统一入口的需求，例如财务处、人事处、学工处、教务处、图书馆等存在各种政策和文件规定，目前在校师生都是从各个部门网站中采取一系列繁琐的查询方法去寻找相应的疑惑解答。目前现有的大多数校园百事通问答方法采取基于知识图谱的方式构建答库，可扩展性和推理性较弱，对新的知识库自适应更新能力较弱。针对此问题，本项目设计研发了一种基于校园大模型的校园智能问答系统，旨在于帮助高校建立统一的高效信息获取平台。  
 　　**基座模型**使用**Internlm2.5-chat-7b** :boom:，**心理模型**使用**Internlm2-chat-1.8b**通过**xtuner**进行SFT微调，部署集成了 **LMdeploy加速推理** 🚀，支持 **ASR 语音生成文字(whisper)**  🎙️，支持**TTS 文字转语音(edge-tts)** 🔊，支持 **RAG 检索增强生成** :floppy_disk:，支持 **Agent（React范式）让大模型拥有调用外部工具的能力** :wrench:，最后支持**数字人根据聊天情况动态变化肢体状态** :hear_no_evil:

### 🛠  技术架构

![image-20240706173454799](/assets/SCSE技术路线.png)

#### 构建心理大模型数据集和微调

本项目参考[Emollm](https://github.com/SmartFlowAI/EmoLLM/blob/main/generate_data/tutorial.md)构建心理微调数据集，感谢Emollm支持

本项目使用[Xtuner](https://github.com/InternLM/xtuner)微调工具+qlora的方法构建新的模型，项目也支持直接通过[LMDeploy](https://github.com/InternLM/LMDeploy)接入现有的心理类llm进行对话

#### RAG

目前只开源了部分pdf文件和txt文件，

针对普通pdf文件，本项目通过使用[Doc2X](https://doc2x.noedgeai.com/)将pdf文件转为了markdown结构化文件，通过项目测试，结构化的markdown的召回效果更佳

针对txt文件，由于txt内容的内容较少，直接使用传统的chunk方法进行embedding存储

针对模式识别的pdf课程文件，构建知识图谱kg和向量数据库，通过混合检索共同回答问题。

#### Agent

Agent是基于[ReAct](https://arxiv.org/abs/2210.03629)范式实现，其核心在于通过整合**推理（Reasoning）**与**行动（Acting）**的功能，以增强模型在解决复杂任务时的能力，具体包括

- **推理(Reasoning)**

  此部分专注于模型的生成推理能力。它基于链式思考（chain-of-thought）的高级提示技术，旨在促使模型在执行任务时能够进行更为深入的思考和逻辑推　　　　　　理。核心要点在于通过这种方法，模型能够在其决策过程中更加有效地跟踪和更新自身的行动策略，并且能够更好地应对在执行过程中可能遇到的各种异常
  情况。

- **行动(Acting)**

  此部分强调模型执行具体行动的能力，这些行动允许模型与外部资源（如知识库或环境）互动，从而获得额外的信息。在ReAct框架中，行动的概念超越了模型输出的直接结果，它指的是模型与外部世界交互的更为广泛的行为，包括但不限于信息检索、执行特定任务的步骤等。此定义扩展了模型能力的理解，强调了模型在与外部世界互动时的动态能力和灵活性。

#### TTS

TTS是一种将文本信息转换成语音输出的技术。在本项目中初步采用[edge-tts](https://kkgithub.com/rany2/edge-tts)，挑选了一个良好的音色用于将LLM的输出文本转换成语音内容，后续会尝试其他TTS（例如GPT-SoVITS）进行再次开发。

#### ASR

ASR是一种将用户的语音输入转换成文本信息输出的技术。在本项目中初步采用[whisper](https://github.com/openai/whisper)，后续可以尝试接入其他的ASR模型（例如FunASR）进行再次开发。

#### 数字人

数字人是一种能够根据不同情况与用户进行虚拟互动的一种技术，能够大大加强用户的体验感。本项目使用three.js将一个glb模型加载到web页面上，目前该模型支持三个动作，分别是休闲状态的动作、用户正在输入的观望动作和聊天状态的动作。后续可以尝试接入更多动作的模型进行再次开发，也会尝试其他的相关数字人技术。

### 📺️ 讲解视频

尚未制作...

### 🎯 使用指南

**配置项目环境**

~~~
git clone https://github.com/626394316/SCSE.git
conda create -n SCSE python=3.10 -y
conda activate SCSE
pip install -r requirements.txt
~~~

**配置项目变量**

~~~
将config.yml中的各项变量换成自己的实际所需
~~~

**启动前端页面**

~~~
cd web_demo
npm install
npm run serve
~~~

登录账号为admin,密码123456

**启动模型**（需要自行配备好lmdeploy环境）

~~~
# 基座模型使用Internlm2_5-chat-7b-int4(需要使用lmdepoly进行量化)
lmdeploy serve api_server  your_main_llm_path \
                            --server-name 127.0.0.1 \
                            --model-name Internlm2_5-chat-7b-int4 \
                            --cache-max-entry-count 0.01 \
                            --server-port 8000
# 心理聊天模型                       
lmdeploy serve api_server your_emo_llm_path \
                            --server-name 127.0.0.1 \
                            --model-name your_emo_llm_name \
                            --cache-max-entry-count 0.01 \
                            --server-port 23333
~~~

**启动后端接口**

~~~
cd SCSE/dealFiles
python common_files.py
python images_files.py
python pr_files.py
cd ..
python qa_mysql.py
uvicorn main:app --host 127.0.0.1 --port 7091 --workers 1 --reload
~~~

**配置mysql环境**

~~~
mysql文件在mysql文件夹中，正常在navicat导入即可
~~~

**配置neo4j数据库**

~~~
尚未开源，还在整理
~~~

### 💕 特别鸣谢

- [InternLM](https://github.com/InternLM/InternLM)
- [xtuner](https://github.com/InternLM/xtuner)
- [LMDeploy](https://github.com/InternLM/LMDeploy)
- [Emollm](https://github.com/SmartFlowAI/EmoLLM/blob/main/generate_data/tutorial.md)

感谢上海人工智能实验室推出的书生·浦语大模型实战营，为我们的项目提供宝贵的技术指导和强大的算力支持。



