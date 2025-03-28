"""
Run `fastapi dev api.py` to start the API server.
"""
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import PlainTextResponse
from note import NoteBook, Note


api = FastAPI()
notebook = NoteBook()


@api.get("/", response_class=PlainTextResponse)
def read_root():
    """Returns the instructions for the API"""
    message = (
        "/static/instructions.html for the main page\n"
        "/list for the list of notes\n"
        "/write?name=NAME&content=CONTENT to add a note\n"
        "/find?term=TERM to search for a note by content\n"
        "/note/Note-Name to read a note by name"
    )
    return message


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
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found")


@api.delete("/note")
def remove(name: str):
    """Removes a note from the notebook"""
    removed = notebook.remove(name)
    if removed:
        return Response(
            content={"message": f'Note "{name}" removed successfully'},
            media_type="application/json",
            status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail="Note not found")


@api.post("/add")
def write(note: Note):
    """
    Adds a Note to the notebook
    Will not allow adding a note with the same name as an existing note
    :param note:
    """
    name = note.name
    if notebook.read(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A note with the name '{name}' already exists.")
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
    if not term:
        raise HTTPException(status_code=400, detail="Invalid search term.")
    notes = notebook.search(term)
    if notes is None:
        raise HTTPException(status_code=404,
                            detail="No notes found with the search term")
    else:
        return {"notes": notes, "term": term}

def app():
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app()
