from fastapi import FastAPI, HTTPException
from note import NoteBook, Note


api = FastAPI()
notebook = NoteBook()


@api.get("/")
def read_root():
    message = ("/static/instructions.html for the main page"
               " /list for the list of notes"
               " /write?name=NAME&content=CONTENT to add a note"
               " /find?term=TERM to search for a note by content"
               " /note/Note-Name to read a note by name")
    return {"message": message}


@api.get("/notes")
def list_notes():
    return {"notes": note.name for note in notebook.list_notes()}


@api.get("/note/{name}")
def read(name: str):
    note = notebook.read(name)
    if note:
        return {"note": note}
    raise HTTPException(status_code=404, detail="Note not found")


@api.delete("/note")
def remove(name: str):
    notebook.remove(name)
    return {"message": f"Note {name} removed successfully"}


@api.post("/add")
def write(note: Note):
    name = note.name
    if notebook.read(name):
        return {"message": f"Note {name} already exists"}
    notebook.add_note(note)
    return {"message": f'Note "{name}" written successfully'}


@api.get("/find")
def find(term: str):
    notes = notebook.search(term)
    if notes:
        return {"term": term, "notes": notes}
    raise HTTPException(status_code=404, detail="No notes found")



