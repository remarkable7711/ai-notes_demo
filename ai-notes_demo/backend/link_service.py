from sqlalchemy.orm import Session
from sqlalchemy import and_
import re
from database import Note, NoteLink

# Markdown内部链接正则：匹配 [[笔记标题]]
LINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")

# 解析笔记内容，提取所有内部链接标题
def extract_outlink_titles(content:str):
    matches = LINK_PATTERN.findall(content)
    return [title.strip() for title in matches]

# 重新构建当前笔记的全部出链关系（每次保存笔记调用）
def rebuild_note_links(db: Session, source_note_id:int, content:str):
    # 1. 删除该笔记旧的全部出链
    db.query(NoteLink).filter(NoteLink.source_note_id == source_note_id).delete()
    # 2. 提取正文内所有 [[xxx]] 链接标题
    target_titles = extract_outlink_titles(content)
    for title in target_titles:
        target_note = db.query(Note).filter(Note.title == title).first()
        if target_note:
            new_link = NoteLink(source_note_id=source_note_id, target_note_id=target_note.id)
            db.add(new_link)
    db.commit()

# 获取【出链列表】：当前笔记向外链接了哪些笔记
def get_out_links(db: Session, note_id:int):
    links = db.query(NoteLink).filter(NoteLink.source_note_id == note_id).all()
    result = []
    for link in links:
        target_note = db.query(Note).filter(Note.id == link.target_note_id).first()
        result.append({"note_id": target_note.id, "title": target_note.title})
    return result

# 获取【反向链接】：哪些笔记链接到当前笔记（核心能力）
def get_back_links(db: Session, note_id:int):
    links = db.query(NoteLink).filter(NoteLink.target_note_id == note_id).all()
    result = []
    for link in links:
        source_note = db.query(Note).filter(Note.id == link.source_note_id).first()
        result.append({"note_id": source_note.id, "title": source_note.title})
    return result