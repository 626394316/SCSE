from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
import os
import shutil
import yaml

with open("../config.yml", 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)
class DataProcess():
    def __init__(self):
        self.base_dir = '../data/pr_data'
        self.embedding_model = HuggingFaceEmbeddings(model_name=configs['embedding_model_path'])
        self.documents_md = []
        self.documents_txt = []
        self.vector_db_dir = "../vector_db/pr_data"

    def split_md(self, text):
        head_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ('#', 'Header 1'),
            ('##', 'Header 2'),
            ('###', 'Header 3'),
        ])
        docs = head_splitter.split_text(text)
        final = []
        for doc in docs:
            header = ''
            if len(doc.metadata) > 0:
                if 'Header 1' in doc.metadata:
                    header += doc.metadata['Header 1']
                if 'Header 2' in doc.metadata:
                    header += ' '
                    header += doc.metadata['Header 2']
                if 'Header 3' in doc.metadata:
                    header += ' '
                    header += doc.metadata['Header 3']
                final.append('{} {}'.format(
                    header, doc.page_content.lower()))
        return final

    def get_md_documents(self, md_path):
        documents = []
        length = 0
        with open(md_path, encoding='utf8') as f:
            text = f.read()
        chunks = self.split_md(text)
        for chunk in chunks:
            new_doc = Document(page_content=chunk, metadata={
                'source': md_path
            })
            length += len(chunk)
            documents.append(new_doc)
        return documents, length

    def save_md_file(self, path):
        documents_md, length = self.get_md_documents(path)
        for doc in documents_md:
            doc.metadata['source'] = doc.metadata['source'].replace('\\', '/')
            self.documents_md.append(doc)
        print("self.documents_md",self.documents_md)

    def build_vectory_db(self):
        # 加载文件
        for file in os.listdir(self.base_dir):
            new_path = os.path.join("../web_demo/public/static/file", file).replace('\\', '/')
            if os.path.exists("../data/pr_data/" + file):
                # 复制文件
                shutil.copy("../data/pr_data/" + file, new_path)
                print(f"文件已从 {'../data/pr_data/' + file} 复制到 {new_path}")
            else:
                print(f"错误：源文件 {'../data/pr_data/' + file} 不存在")

            if file.endswith('.md'):
                self.save_md_file(new_path)

        vectorstore = FAISS.from_documents(documents=self.documents_txt+self.documents_md,
                                           embedding=self.embedding_model)

        vectorstore.save_local(self.vector_db_dir)
        return vectorstore

    def load_vectory_db(self):

        if not os.path.exists(self.vector_db_dir):
            vectorstore = self.build_vectory_db()
        else:
            vectorstore = FAISS.load_local(self.vector_db_dir, self.embedding_model,
                                           allow_dangerous_deserialization=True)

        return vectorstore


if __name__ == '__main__':
    dp = DataProcess()
    vectorstore = dp.load_vectory_db()
    query = "模式识别的会议有什么"
    docs = vectorstore.similarity_search(query,k=3)
    print('------')
    for i in docs:
        print(i)
