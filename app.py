from flask import Flask, request, render_template, redirect, url_for
from note import NoteBook

app = Flask(__name__)
notebook = NoteBook()

@app.route('/')
def index():
    query = request.args.get('query', '')
    notes = notebook.search(query) if query else notebook.list_notes()
    return render_template('index.html', notes=notes, query=query)

@app.route('/note/<name>')
def note_detail(name):
    note = notebook.read(name)
    if note:
        return render_template('note.html', note=note)
    return "Note not found", 404

@app.route('/write', methods=['POST'])
def write_note():
    name = request.form['name']
    content = request.form['content']
    if notebook.read(name):
        return "Note already exists", 400
    notebook.write(name, content)
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    notes = notebook.search(query)
    return render_template('index.html', notes=notes, query=query)

if __name__ == '__main__':
    app.run(debug=True)