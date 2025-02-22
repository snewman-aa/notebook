"""
Relies on the FastAPI server from api.py to provide the API endpoints for the
Streamlit app.
Before running this streamlit, make sure the FastAPI server is running on port
8000.
"""

import streamlit as st
import requests
from functools import partial


API_URL = "http://localhost:8000"

api_get = partial(requests.get)
api_post = partial(requests.post)

get_names = partial(api_get, f"{API_URL}/list")
get_notes = partial(api_get, f"{API_URL}/notes")
search_notes = partial(api_get, f"{API_URL}/find")

read_note = lambda name: api_get(f"{API_URL}/note/{name}")

write_note = partial(api_post, f"{API_URL}/add")


def get_note_names():
    response = get_names()
    if response.status_code != 200:
        return "Failed to display notes"
    content = response.json()
    return list(content.get("notes"))


def display_note():
    if not (note_name := st.session_state.selected_note):
        return
    response = read_note(note_name)
    if handle_api_error(response):
        return
    note = response.json()
    st.session_state.title_box = note.get("name")
    st.session_state.content_box = note.get("content")


def display_search_result(note):
    st.session_state.selected_note = note
    display_note()


def add_note(name: str, content: str):
    new_note = {'name': name, 'content': content}
    response = write_note(json=new_note)
    if handle_api_error(response):
        return
    st.success(f'Note "{name}" added successfully')


def handle_api_error(response):
    if response.status_code is None:
        st.error("Could not connect to the server. Run apy.py first.")
        return True
    elif response.status_code == 400:
        st.warning(f"Bad request: {response.json().get('detail')}")
        return True
    elif response.status_code == 404:
        st.error(f"Error: {response.json().get('detail')}")
        return True
    elif 401 <= response.status_code < 500:
        st.error(f"Error ({response.status_code}):"
                 f" {response.json().get('detail')}")
        return True
    return False


st.title("Notebook App")

if "title_box" not in st.session_state:
    st.session_state.title = ""
if "content_box" not in st.session_state:
    st.session_state.content = ""
if "selected_note" not in st.session_state:
    st.session_state.selected_note = ""


view_tab, add_tab = st.tabs(["View Notes", "Add Note"])

with view_tab:
    st.session_state.selected_note = (
        st.selectbox("Select a note",
                     get_note_names(),
                     key="view",
                     placeholder="Select a note",
                     help="Select a note to view its content."))
    st.button("View Note", on_click=display_note)
    title = st.text_input("Title", key="title_box", disabled=True,)
    content = st.text_area("Content", key="content_box", disabled=True)

with add_tab:
    name = st.text_input("Name")
    content = st.text_area("Content")
    if st.button("Add Note"):
        add_note(name, content)


with st.sidebar:
    search_term = st.text_input("Search",
                                key="search_bar",
                                placeholder="Search Notes")
    if st.button("Search", key="search"):
        if not search_term:
            st.warning("Please enter a search term.")
        else:
            response = search_notes(params={"term": search_term})
            if handle_api_error(response):
                pass
            else:
                notes = response.json().get("notes")
                if notes:
                    st.write(f"Notes containing '{search_term}':")
                    for note in notes:
                        st.button(note, key=f"search_result_{note}",
                                  on_click=display_search_result, args=(note,))
                else:
                    st.write(f"No notes found containing '{search_term}'.")
