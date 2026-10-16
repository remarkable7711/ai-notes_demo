const API_BASE = "http://127.0.0.1:8000";
let currentNoteId = null;
let selectedTextRange = null;

// 加载笔记列表
async function loadNoteList(){
    const res = await fetch(`${API_BASE}/notes`);
    const notes = await res.json();
    const dom = document.getElementById("noteList");
    dom.innerHTML = "";
    notes.forEach(n=>{
        const div = document.createElement("div");
        div.innerText = n.title;
        div.onclick = ()=>loadNote(n.id);
        dom.appendChild(div);
    })
}

// 加载单条笔记
async function loadNote(noteId){
    currentNoteId = noteId;
    const res = await fetch(`${API_BASE}/notes/${noteId}`);
    const note = await res.json();
    document.getElementById("noteTitle").value = note.title;
    document.getElementById("noteEditor").value = note.content;
    loadLinkPanel(noteId);
}

// 加载出链、反向链接面板
async function loadLinkPanel(noteId){
    const outRes = await fetch(`${API_BASE}/notes/${noteId}/outlinks`);
    const outLinks = await outRes.json();
    document.getElementById("outlinkList").innerHTML = outLinks.map(x=>`<div>${x.title}</div>`).join("");

    const backRes = await fetch(`${API_BASE}/notes/${noteId}/backlinks`);
    const backLinks = await backRes.json();
    document.getElementById("backlinkList").innerHTML = backLinks.map(x=>`<div>${x.title}</div>`).join("");
}

async function createNewNote(){
    const title = prompt("输入新笔记标题");
    if(!title) return;
    await fetch(`${API_BASE}/notes`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({title, content:""})
    })
    loadNoteList();
}

async function saveNote(){
    const title = document.getElementById("noteTitle").value;
    const content = document.getElementById("noteEditor").value;
    if(!currentNoteId){
        alert("请先选中笔记");return;
    }
    await fetch(`${API_BASE}/notes/${currentNoteId}`,{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({title, content})
    })
    loadNoteList();
    loadLinkPanel(currentNoteId);
    alert("已保存，链接关系自动更新");
}

async function deleteNote(){
    if(!currentNoteId || !confirm("确认删除笔记？")) return;
    await fetch(`${API_BASE}/notes/${currentNoteId}`,{method:"DELETE"});
    currentNoteId=null;
    document.getElementById("noteTitle").value="";
    document.getElementById("noteEditor").value="";
    loadNoteList();
}

// ========== 勾选文本，插入内部链接（题目核心功能） ==========
function insertInternalLink(){
    const editor = document.getElementById("noteEditor");
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    selectedTextRange = {start, end};
    openModal();
}

async function openModal(){
    document.getElementById("linkModal").style.display="block";
    const res = await fetch(`${API_BASE}/notes`);
    const notes = await res.json();
    const modalDom = document.getElementById("modalNoteList");
    modalDom.innerHTML = "";
    notes.forEach(n=>{
        const item = document.createElement("div");
        item.innerHTML = `<input type="checkbox" value="${n.title}" id="chk-${n.id}"> ${n.title}`;
        modalDom.appendChild(item);
    })
}

function closeModal(){
    document.getElementById("linkModal").style.display="none";
}

function confirmInsertLink(){
    const editor = document.getElementById("noteEditor");
    const checkboxes = document.querySelectorAll("#modalNoteList input:checked");
    const targetTitles = Array.from(checkboxes).map(cb=>cb.value);
    if(targetTitles.length ===0){
        alert("请勾选至少一条笔记");return;
    }
    // 拼接 [[笔记名]]
    const linkStr = targetTitles.map(t=>`[[${t}]]`).join(" ");
    const originText = editor.value;
    const {start, end} = selectedTextRange;
    // 替换选中区域文本为链接
    const newText = originText.substring(0, start)+linkStr + originText.substring(end);
    editor.value = newText;
    closeModal();
}

// 初始化
loadNoteList();
</script>