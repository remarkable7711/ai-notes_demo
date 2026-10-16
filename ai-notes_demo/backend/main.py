from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import link_service
import schemas
from database import get_db

app = FastAPI(title="AI Notes Demo 对标WeKnora笔记")

# ========= 笔记基础CRUD接口 =========
@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db:Session=Depends(get_db)):
    res = crud.create_note(db, note)
    # 创建后，解析并生成出链关系
    link_service.rebuild_note_links(db, res.id, res.content)
    return res

@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def read_note(note_id:int, db:Session=Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note

@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def modify_note(note_id:int, note_update:schemas.NoteUpdate, db:Session=Depends(get_db)):
    note = crud.update_note(db, note_id, note_update)
    if not note:
        raise HTTPException(status_code=404)
    # 更新笔记后，重新解析出链
    link_service.rebuild_note_links(db, note.id, note.content)
    return note

@app.delete("/notes/{note_id}")
def remove_note(note_id:int, db:Session=Depends(get_db)):
    ok = crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404)
    return {"msg":"删除成功"}

# ========= 链接API：出链、反向链接 =========
@app.get("/notes/{note_id}/outlinks")
def get_note_outlinks(note_id:int, db:Session=Depends(get_db)):
    return link_service.get_out_links(db, note_id)

@app.get("/notes/{note_id}/backlinks")
def get_note_backlinks(note_id:int, db:Session=Depends(get_db)):
    return link_service.get_back_links(db, note_id)

@app.get("/notes", response_model=List[schemas.NoteResponse])
def list_all_notes(db:Session=Depends(get_db)):
    return crud.get_all_notes(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)