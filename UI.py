"""
UI file — Streamlit screens and buttons only.

All array / DSA work lives in DSA_Concept.py.
This file only CALLS those methods. It does not do append/pop itself.
"""
import streamlit as st
from DSA_Concept import PlaylistManager


def init_state():
    # Keep the DSA manager in session so data stays while you click buttons
    if "manager" not in st.session_state:
        st.session_state.manager = PlaylistManager()
        st.session_state.playing = None  # which song is playing now
        st.session_state.show_rename = False
        st.session_state.show_delete = False


def play_song(song):
    st.session_state.playing = song


st.set_page_config(page_title="Pulse — Playlist Manager", page_icon="🎵", layout="wide")
init_state()

manager = st.session_state.manager

# ——— Sidebar ———
with st.sidebar:
    st.title("Pulse")
    st.caption("Playlist Manager (Array DSA)")
    st.divider()

    with st.form("new_playlist", clear_on_submit=True):
        name = st.text_input("New playlist name", placeholder="e.g. Workout Mix")
        if st.form_submit_button("Create", use_container_width=True):
            # DSA call: create_playlist uses append on the playlists array
            created = manager.create_playlist(name)
            if not created:
                st.warning("Name is required")
            else:
                st.success(f'Created "{name}"')
                st.rerun()

    st.subheader("Your playlists")
    if manager.playlists == []:
        st.info("No playlists yet. Create one above.")
    else:
        # Loop the playlists ARRAY by index
        for i, p in enumerate(manager.playlists):
            label = f"{p.name}  ({p.size()})"
            is_current = i == manager.current_index
            if st.button(
                label,
                key=f"pl_{i}",
                use_container_width=True,
                type="primary" if is_current else "secondary",
            ):
                # DSA call: select by index in the array
                manager.select_playlist(i)
                st.rerun()

# ——— Main: current playlist ———
playlist = manager.get_current()
current_i = manager.current_index

if not playlist:
    st.header("Start your first playlist")
    st.write("Create one from the sidebar to begin collecting tracks.")
else:
    songs = playlist.get_all()  # DSA: get the songs array
    head_l, head_r = st.columns([3, 2])
    with head_l:
        st.header(playlist.name)
        st.caption(f"{playlist.size()} track{'s' if playlist.size() != 1 else ''} in this playlist")
    with head_r:
        c1, c2, c3 = st.columns(3)
        if c1.button("Play all", use_container_width=True, disabled=playlist.size() == 0):
            play_song(songs[0])
            st.rerun()
        if c2.button("Rename", use_container_width=True):
            st.session_state.show_rename = True
        if c3.button("Delete", use_container_width=True, type="primary"):
            st.session_state.show_delete = True

    if st.session_state.get("show_rename"):
        with st.form("rename_form"):
            new_name = st.text_input("Rename playlist", value=playlist.name)
            col_a, col_b = st.columns(2)
            save = col_a.form_submit_button("Save", use_container_width=True)
            cancel = col_b.form_submit_button("Cancel", use_container_width=True)
            if cancel:
                st.session_state.show_rename = False
                st.rerun()
            if save:
                # DSA call: rename playlist at current index
                if manager.rename_playlist(current_i, new_name):
                    st.session_state.show_rename = False
                    st.rerun()
                else:
                    st.warning("Name is required")

    if st.session_state.get("show_delete"):
        st.warning(f'Delete "{playlist.name}"? This cannot be undone.')
        d1, d2 = st.columns(2)
        if d1.button("Confirm delete", use_container_width=True, type="primary"):
            # DSA call: delete_playlist uses pop(index) on playlists array
            manager.delete_playlist(current_i)
            st.session_state.show_delete = False
            st.rerun()
        if d2.button("Cancel delete", use_container_width=True):
            st.session_state.show_delete = False
            st.rerun()

    if playlist.size() == 0:
        st.info("This playlist is empty. Add songs from the library below.")
    else:
        # Loop songs ARRAY by index (index is what DSA delete/move use)
        for i, song in enumerate(songs):
            cols = st.columns([4, 1.2, 0.7, 0.7, 1])
            playing = (
                st.session_state.playing
                and st.session_state.playing["id"] == song["id"]
            )
            mark = "▶ " if playing else ""
            cols[0].markdown(
                f"**{mark}{song['title']}**  \n"
                f"{song['artist']} · `{song['genre']}`"
            )
            if cols[1].button("Play", key=f"play_{i}_{song['id']}", use_container_width=True):
                play_song(song)
                st.rerun()
            if cols[2].button("↑", key=f"up_{i}", disabled=i == 0, use_container_width=True):
                # DSA call: swap with index above
                playlist.move_up(i)
                st.rerun()
            if cols[3].button(
                "↓",
                key=f"down_{i}",
                disabled=i == playlist.size() - 1,
                use_container_width=True,
            ):
                # DSA call: swap with index below
                playlist.move_down(i)
                st.rerun()
            if cols[4].button("Remove", key=f"rm_{i}", use_container_width=True):
                # DSA call: remove_song_at uses pop(index)
                playlist.remove_song_at(i)
                st.rerun()

st.divider()

# ——— Library ———
st.subheader("Song library")
st.caption("Browse and add tracks to your playlist")
query = st.text_input(
    "Search",
    placeholder="Search title, artist or genre",
    label_visibility="collapsed",
)
# DSA call: search loops the library array
library = manager.search_library(query)

if not library:
    st.info("No songs match your search.")
else:
    for song in library:
        cols = st.columns([4, 1.2, 1.2])
        cols[0].markdown(
            f"**{song['title']}**  \n{song['artist']} · `{song['genre']}`"
        )
        if cols[1].button("Play", key=f"lib_play_{song['id']}", use_container_width=True):
            play_song(song)
            st.rerun()
        already = playlist.has_song(song["id"]) if playlist else False
        add_label = "Added" if already else "Add"
        if cols[2].button(
            add_label,
            key=f"add_{song['id']}",
            disabled=not playlist or already,
            use_container_width=True,
        ):
            # DSA call: add_song uses append on the playlist songs array
            playlist.add_song(song)
            st.toast(f'Added "{song["title"]}"')
            st.rerun()

# ——— Player ———
st.divider()
playing = st.session_state.playing
if playing:
    st.markdown(f"**Now playing:** {playing['title']} — {playing['artist']}")
    st.audio(playing["url"], format="audio/mp3", autoplay=True)
else:
    st.caption("Pick a song to play")
