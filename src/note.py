from collections import defaultdict
from pydantic import BaseModel

class Note(BaseModel):
    name: str
    content: str


class NoteBook:
    def __init__(self):
        self._notes = defaultdict(Note)

    @staticmethod
    def _create_note(name: str, content: str) -> Note:
        """
        Create a note (for adding to the notebook)
        :param name: Name of the note
        :param content: Content of the note
        """
        return Note(name=name, content=content)

    @property
    def __len__(self):
        return len(self._notes)

    def add_note(self, note: Note):
        """
        Add a note to the notebook
        :param note: Note object to add
        """
        self._notes.update({note.name: note})

    def remove(self, name: str) -> Note | bool:
        """
        Remove a note from the notebook.
        :param name: Name of the note to remove
        :return: Deleted note or False if note not found
        """
        if name not in self._notes:
            return False
        return self._notes.pop(name)


    def write(self, name: str, content: str):
        """
        Write a note to the notebook,
        creating a new note object and adding it to the notebook.
        :param name: Name of the note
        :param content: Content of the note
        """
        note = self._create_note(name, content)
        self.add_note(note)

    def list_notes(self) -> list[Note]:
        """
        List all notes in the notebook
        :return: List of all Note objects in the notebook
        """
        return list(self._notes.values())

    def search(self, query: str) -> list[str] | None:
        """
        Search for notes in the notebook by content.
        :param query:
        :return: A list of note **names** whose content contains the query
        """
        notes = [note.name for note in self._notes.values() if query in note.content]
        if notes:
            return notes
        return None

    def read(self, name: str) -> Note | None:
        """
        Read a note from the notebook.
        :param name:
        :return: Note object if found, otherwise None
        """
        return self._notes.get(name)