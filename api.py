from fastapi import FastAPI, HTTPException
from note import NoteBook, Note


api = FastAPI()
notebook = NoteBook()


@api.get("/")
def read_root():
    """Returns the instructions for the API"""
    message = ("/static/instructions.html for the main page"
               " /list for the list of notes"
               " /write?name=NAME&content=CONTENT to add a note"
               " /find?term=TERM to search for a note by content"
               " /note/Note-Name to read a note by name")
    return {"message": message}


@api.get("/notes")
def list_notes():
    """Lists all the notes in the notebook"""
    return {"notes": [note for note in notebook.list_notes()]}

@api.get("/list")
def list_note_names():
    """Lists all the names of the notes in the notebook"""
    return {"notes": [note.name for note in notebook.list_notes()]}


@api.get("/note/{name}")
def read(name: str):
    """Reads a note from the notebook"""
    note = notebook.read(name)
    if note:
        return {"note": note}
    raise HTTPException(status_code=404, detail="Note not found")


@api.delete("/note")
def remove(name: str):
    """Removes a note from the notebook"""
    notebook.remove(name)
    return {"message": f'Note "{name}" removed successfully'}


@api.post("/add")
def write(note: Note):
    """
    Adds a Note to the notebook
    Will not allow adding a note with the same name as an existing note
    :param note:
    """
    name = note.name
    if notebook.read(name):
        return {"message": f'Note "{name}" already exists'}
    notebook.add_note(note)
    return {"message": f'Note "{name}" written successfully'}


@api.get("/find")
def find(term: str):
    """
    Returns the names of all the notes that contain the search term in their
    content
    :param term:
    :return: list of note names
    """
    notes = notebook.search(term)
    if notes:
        return {"term": term, "notes": notes}
    raise HTTPException(status_code=404, detail="No notes found")



