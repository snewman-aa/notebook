from flask import Flask, request, render_template, redirect, url_for
from note import NoteBook
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
notebook = NoteBook()

@app.route('/')
def index():
    """
    This is the main page of the app.
    It lists all the notes if there is no query,
    otherwise it lists the notes whose contents contain the query.
    """
    query = request.args.get('query', '')
    if query:
        note_names = notebook.search(query)
        notes = [notebook.read(name) for name in note_names]
    else:
        notes = notebook.list_notes()
    if not notes:
        return render_template('index.html', notes=[], query=query)
    return render_template('index.html', notes=notes, query=query)

@app.route('/note/<name>')
def note_detail(name):
    """
    Displays the content of a note.
    :param name:
    """
    note = notebook.read(name)
    if note:
        return render_template('note.html', note=note)
    return "Note not found", 404

@app.route('/write', methods=['POST'])
def write_note():
    """
    Adds a note to the notebook.
    :return:
    """
    name = request.form['name']
    content = request.form['content']
    if notebook.read(name):
        return "Note already exists", 400
    notebook.write(name, content)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    """
    This isn't actually used in the app,
    but it's here to be accessible via the API.
    """
    query = request.form['query']
    note_names = notebook.search(query)
    notes = [notebook.read(name) for name in note_names]
    if not notes:
        return "No notes found", 404
    return render_template('index.html', notes=notes, query=query)


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()