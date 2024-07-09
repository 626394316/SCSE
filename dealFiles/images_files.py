import os
import yaml
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

with open("../config.yml", 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)
class ImageProcess():
    def __init__(self):
        self.folder_path = "../web_demo/src/assets/llm_img"
        self.image_vector_db_dir = "../vector_db/image_data"
        self.embedding_model = HuggingFaceEmbeddings(model_name=configs['embedding_model_path'])
        self.images = []
    def build_image_vectory_db(self):
        # 检查路径是否存在
        if os.path.exists(self.folder_path):
            # 列出文件夹中的所有条目
            for img in os.listdir(self.folder_path):
                # 构造完整的文件路径
                img_path = os.path.join(self.folder_path, img).replace('\\','/')
                if img.lower().endswith(('.jpg', '.png')):
                    img_info = Document(page_content=img.split('.')[0], metadata={
                        'source': img_path
                    })
                    self.images.append(img_info)
            print("存取图片文件成功")
        else:
            print("指定的文件夹不存在")
        vectorstore = FAISS.from_documents(
            documents=self.images,
            embedding=self.embedding_model,
        )
        vectorstore.save_local(self.image_vector_db_dir)
        return vectorstore

    def load_vectory_db(self):

        if not os.path.exists(self.image_vector_db_dir):
            vectorstore = self.build_image_vectory_db()
        else:
            vectorstore = FAISS.load_local(self.image_vector_db_dir, self.embedding_model,
                                           allow_dangerous_deserialization=True)
        return vectorstore

if __name__ == '__main__':
    ip = ImageProcess()
    vectorstore = ip.load_vectory_db()
    query = "帮我生成一张华侨大学的logo图片"
    docs = vectorstore.similarity_search(query,k=3)
    print('------')
    for i in docs:
        print(i)


