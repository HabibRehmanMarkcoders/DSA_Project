"""Music Playlist Manager — Streamlit UI with in-memory CRUD (no backend API)."""
import streamlit as st

URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{}.mp3"
_RAW = [
    ("Neon Rain", "Luna Vale", "Synthwave"),
    ("Golden Hour", "The Paper Kites", "Indie"),
    ("Midnight Drive", "Kora Blue", "Electronic"),
    ("Slow Burn", "Andre Cole", "R&B"),
    ("Paper Planes", "Mika Rowe", "Pop"),
    ("Salt & Static", "Hollow Tide", "Rock"),
    ("Velvet Sky", "Nova Reyes", "Chill"),
    ("Run Wild", "The Northern Lights", "Alternative"),
    ("Afterglow", "Sable", "Dream Pop"),
    ("City of Glass", "Echo Harbor", "Electronic"),
    ("Blue Monday Sun", "Jonah Frost", "Folk"),
    ("Lantern", "Maya Osei", "Acoustic"),
]


def seed_songs():
    return [
        {"id": i + 1, "title": t, "artist": a, "genre": g, "url": URL.format(i + 1)}
        for i, (t, a, g) in enumerate(_RAW)
    ]


def seed_playlists():
    return {
        1: {"id": 1, "name": "Late Night Drive", "song_ids": [3, 1, 10]},
        2: {"id": 2, "name": "Morning Coffee", "song_ids": [2, 12, 11, 7]},
    }


def init_state():
    if "songs" not in st.session_state:
        st.session_state.songs = seed_songs()
        st.session_state.song_by_id = {s["id"]: s for s in st.session_state.songs}
        st.session_state.playlists = seed_playlists()
        st.session_state.next_id = 3
        st.session_state.current_id = 1
        st.session_state.playing = None  # song dict or None


def current_playlist():
    pid = st.session_state.current_id
    if pid is None:
        return None
    return st.session_state.playlists.get(pid)


def playlist_songs(playlist):
    by_id = st.session_state.song_by_id
    return [by_id[i] for i in playlist["song_ids"] if i in by_id]


def play_song(song):
    st.session_state.playing = song


st.set_page_config(page_title="Pulse — Playlist Manager", page_icon="🎵", layout="wide")
init_state()

# ——— Sidebar ———
with st.sidebar:
    st.title("Pulse")
    st.caption("Playlist Manager")
    st.divider()

    with st.form("new_playlist", clear_on_submit=True):
        name = st.text_input("New playlist name", placeholder="e.g. Workout Mix")
        if st.form_submit_button("Create", use_container_width=True):
            name = (name or "").strip()
            if not name:
                st.warning("Name is required")
            else:
                pid = st.session_state.next_id
                st.session_state.playlists[pid] = {
                    "id": pid,
                    "name": name,
                    "song_ids": [],
                }
                st.session_state.next_id = pid + 1
                st.session_state.current_id = pid
                st.success(f"Created “{name}”")
                st.rerun()

    st.subheader("Your playlists")
    playlists = list(st.session_state.playlists.values())
    if not playlists:
        st.info("No playlists yet. Create one above.")
    else:
        for p in playlists:
            label = f"{p['name']}  ({len(p['song_ids'])})"
            if st.button(
                label,
                key=f"pl_{p['id']}",
                use_container_width=True,
                type="primary" if p["id"] == st.session_state.current_id else "secondary",
            ):
                st.session_state.current_id = p["id"]
                st.rerun()

# ——— Main: current playlist ———
playlist = current_playlist()

if not playlist:
    st.header("Start your first playlist")
    st.write("Create one from the sidebar to begin collecting tracks.")
else:
    songs = playlist_songs(playlist)
    head_l, head_r = st.columns([3, 2])
    with head_l:
        st.header(playlist["name"])
        st.caption(f"{len(songs)} track{'s' if len(songs) != 1 else ''} in this playlist")
    with head_r:
        c1, c2, c3 = st.columns(3)
        if c1.button("Play all", use_container_width=True, disabled=not songs):
            play_song(songs[0])
            st.rerun()
        if c2.button("Rename", use_container_width=True):
            st.session_state.show_rename = True
        if c3.button("Delete", use_container_width=True, type="primary"):
            st.session_state.show_delete = True

    if st.session_state.get("show_rename"):
        with st.form("rename_form"):
            new_name = st.text_input("Rename playlist", value=playlist["name"])
            col_a, col_b = st.columns(2)
            save = col_a.form_submit_button("Save", use_container_width=True)
            cancel = col_b.form_submit_button("Cancel", use_container_width=True)
            if cancel:
                st.session_state.show_rename = False
                st.rerun()
            if save:
                new_name = (new_name or "").strip()
                if not new_name:
                    st.warning("Name is required")
                else:
                    playlist["name"] = new_name
                    st.session_state.show_rename = False
                    st.rerun()

    if st.session_state.get("show_delete"):
        st.warning(f'Delete “{playlist["name"]}”? This cannot be undone.')
        d1, d2 = st.columns(2)
        if d1.button("Confirm delete", use_container_width=True, type="primary"):
            del st.session_state.playlists[playlist["id"]]
            remaining = list(st.session_state.playlists.keys())
            st.session_state.current_id = remaining[0] if remaining else None
            st.session_state.show_delete = False
            st.rerun()
        if d2.button("Cancel delete", use_container_width=True):
            st.session_state.show_delete = False
            st.rerun()

    if not songs:
        st.info("This playlist is empty. Add songs from the library below.")
    else:
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
            if cols[1].button("Play", key=f"play_{song['id']}", use_container_width=True):
                play_song(song)
                st.rerun()
            if cols[2].button("↑", key=f"up_{song['id']}", disabled=i == 0, use_container_width=True):
                ids = playlist["song_ids"]
                ids[i - 1], ids[i] = ids[i], ids[i - 1]
                st.rerun()
            if cols[3].button(
                "↓",
                key=f"down_{song['id']}",
                disabled=i == len(songs) - 1,
                use_container_width=True,
            ):
                ids = playlist["song_ids"]
                ids[i + 1], ids[i] = ids[i], ids[i + 1]
                st.rerun()
            if cols[4].button("Remove", key=f"rm_{song['id']}", use_container_width=True):
                playlist["song_ids"].remove(song["id"])
                st.rerun()

st.divider()

# ——— Library ———
st.subheader("Song library")
st.caption("Browse and add tracks to your playlist")
query = st.text_input("Search", placeholder="Search title, artist or genre", label_visibility="collapsed")
q = (query or "").lower().strip()
library = [
    s
    for s in st.session_state.songs
    if not q or q in (s["title"] + s["artist"] + s["genre"]).lower()
]

if not library:
    st.info("No songs match your search.")
else:
    in_ids = set(playlist["song_ids"]) if playlist else set()
    for song in library:
        cols = st.columns([4, 1.2, 1.2])
        cols[0].markdown(
            f"**{song['title']}**  \n{song['artist']} · `{song['genre']}`"
        )
        if cols[1].button("Play", key=f"lib_play_{song['id']}", use_container_width=True):
            play_song(song)
            st.rerun()
        already = song["id"] in in_ids
        add_label = "Added" if already else "Add"
        if cols[2].button(
            add_label,
            key=f"add_{song['id']}",
            disabled=not playlist or already,
            use_container_width=True,
        ):
            playlist["song_ids"].append(song["id"])
            st.toast(f"Added “{song['title']}”")
            st.rerun()

# ——— Player ———
st.divider()
playing = st.session_state.playing
if playing:
    st.markdown(f"**Now playing:** {playing['title']} — {playing['artist']}")
    st.audio(playing["url"], format="audio/mp3", autoplay=True)
else:
    st.caption("Pick a song to play")
