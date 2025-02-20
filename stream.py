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


def display_note(note_name: str, display_name, display_content):
    if not note_name:
        return
    response = read_note(note_name)
    if handle_api_error(response):
        return
    note = response.json()
    display_name(note.get('name'))
    display_content(note.get('content'))


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


view_tab, add_tab = st.tabs(["View Notes", "Add Note"])

with view_tab:
    selected_note = st.selectbox("Select a note",
                                 get_note_names(),
                                 key="view",
                                 placeholder="Select a note")
    display_note(selected_note, view_tab.header, view_tab.write)

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
                    st.header(f"Notes containing '{search_term}'")
                    for note in notes:
                        st.write(note)
                else:
                    st.write(f"No notes found containing '{search_term}'.")
