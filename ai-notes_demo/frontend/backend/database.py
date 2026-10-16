from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 笔记主表
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text) # Markdown笔记正文，支持[[笔记名]]内部链接

# 笔记链接关系表：存储A笔记【出链】指向B笔记
class NoteLink(Base):
    __tablename__ = "note_links"
    id = Column(Integer, primary_key=True)
    source_note_id = Column(Integer, ForeignKey("notes.id")) # 源笔记（出链方）
    target_note_id = Column(Integer, ForeignKey("notes.id")) # 目标笔记（被链接）

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()