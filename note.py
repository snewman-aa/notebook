from collections import defaultdict
from pydantic import BaseModel

class Note(BaseModel):
    name: str
    content: str


class NoteBook:
    def __init__(self):
        self._notes = defaultdict(Note)

    @staticmethod
    def _create_note(name: str, content: str):
        return Note(name=name, content=content)

    @property
    def __len__(self):
        return len(self._notes)

    def add_note(self, note: Note):
        self._notes.update({note.name: note})

    def remove(self, name: str):
        if name not in self._notes:
            return False
        return self._notes.pop(name)


    def write(self, name: str, content: str):
        note = self._create_note(name, content)
        self.add_note(note)

    def list_notes(self):
        return list(self._notes.values())

    def search(self, query: str):
        notes = [note.name for note in self._notes.values() if query in note.content]
        if notes:
            return notes
        return None

    def read(self, name: str):
        return self._notes.get(name)