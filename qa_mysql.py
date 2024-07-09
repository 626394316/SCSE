import pymysql
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from pydantic import BaseModel
from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# 创建app实例
app = FastAPI()

# 允许跨域资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

# 数据库连接
pymysql.install_as_MySQLdb()
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/historydata?charset=utf8mb4')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = SessionLocal()
# 创建数据库模型
Base = sqlalchemy.orm.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NewHistory(Base):
    # 定义表名
    __tablename__ = 'qa_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    talk_id = Column(Integer, nullable=False)
    talk_time = Column(String(255), nullable=False)
    question = Column(String(9000), nullable=False)
    answer = Column(String(9000), nullable=False)
    message = Column(String(255), nullable=True)
    audio = Column(String(255), nullable=True)


class CreatHistory(BaseModel):
    talk_id: int = 0
    talk_time: str = None
    question: str = None
    answer: str = None
    message: str = None
    audio: str = ""


class DeleteHistory(BaseModel):
    talk_id: int


class RenameHistory(BaseModel):
    id: int
    message: str


# 得到聊天记录
@app.get("/get_history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(NewHistory).order_by(NewHistory.talk_id.desc()).all()
    db.close()
    return history


# 新增聊天记录
@app.post("/add_history")
async def add_history(history: CreatHistory, db: Session = Depends(get_db)):
    HistoryData = NewHistory(talk_id=history.talk_id, talk_time=history.talk_time,
                             question=history.question, answer=history.answer, message=history.message)
    db.add(HistoryData)
    db.commit()
    db.refresh(HistoryData)
    db.close()
    return {"message": "存储聊天记录成功", "id": HistoryData.id}


# 删除整个聊天记录
@app.delete("/delete_history/{talk_id}")
async def delete_history(talk_id: int, db: Session = Depends(get_db)):
    historys = db.query(NewHistory).filter(NewHistory.talk_id == talk_id).all()
    for history in historys:
        db.delete(history)
    db.commit()
    db.close()
    return "删除聊天记录成功"


# 删除单个聊天记录
@app.delete("/delete_chat/{id}")
async def delete_chat(id: int, db: Session = Depends(get_db)):
    chat = db.query(NewHistory).filter(NewHistory.id == id).first()
    db.delete(chat)
    db.commit()
    db.close()
    return "删除对话记录成功"


# 重命名聊天记录
@app.post('/rename_chat')
async def rename_chat(data: RenameHistory, db: Session = Depends(get_db)):
    print(data)
    chat = db.query(NewHistory).filter(NewHistory.id == data.id).first()

    if chat:
        chat.message = data.message
        db.commit()
        db.close()
        return "重命名成功"


if __name__ == "__main__":
    uvicorn.run("qa_mysql:app", host="127.0.0.1", port=7090, reload=True)
