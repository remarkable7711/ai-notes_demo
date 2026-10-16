from sqlalchemy.orm import Session
from database import Note
from schemas import NoteCreate, NoteUpdate

# 创建笔记
def create_note(db: Session, note: NoteCreate):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# 获取单条笔记
def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

# 获取全部笔记
def get_all_notes(db: Session):
    return db.query(Note).all()

# 修改笔记
def update_note(db: Session, note_id:int, note_update:NoteUpdate):
    db_note = get_note(db, note_id)
    if not db_note:
        return None
    db_note.title = note_update.title
    db_note.content = note_update.content
    db.commit()
    db.refresh(db_note)
    return db_note

# 删除笔记
def delete_note(db: Session, note_id:int):
    db_note = get_note(db, note_id)
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True