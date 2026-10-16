from pydantic import BaseModel
from typing import List, Optional

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    class Config:
        orm_mode = True

# 链接返回结构
class NoteLinkItem(BaseModel):
    source_id: int
    target_id: int

class BackLinkResponse(BaseModel):
    note_id: int
    title: str