"""Music Playlist Manager - Flask REST API + static frontend (in-memory data)."""
from flask import Flask, jsonify, request

app = Flask(__name__, static_folder="static", static_url_path="")

# Dummy library: free sample tracks from SoundHelix (royalty-free demo music)
URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{}.mp3"
_raw = [
    ("Neon Rain", "Luna Vale", "Synthwave"), ("Golden Hour", "The Paper Kites", "Indie"),
    ("Midnight Drive", "Kora Blue", "Electronic"), ("Slow Burn", "Andre Cole", "R&B"),
    ("Paper Planes", "Mika Rowe", "Pop"), ("Salt & Static", "Hollow Tide", "Rock"),
    ("Velvet Sky", "Nova Reyes", "Chill"), ("Run Wild", "The Northern Lights", "Alternative"),
    ("Afterglow", "Sable", "Dream Pop"), ("City of Glass", "Echo Harbor", "Electronic"),
    ("Blue Monday Sun", "Jonah Frost", "Folk"), ("Lantern", "Maya Osei", "Acoustic"),
]
SONGS = [{"id": i + 1, "title": t, "artist": a, "genre": g, "url": URL.format(i + 1)}
         for i, (t, a, g) in enumerate(_raw)]
SONG_BY_ID = {s["id"]: s for s in SONGS}

PLAYLISTS = {
    1: {"id": 1, "name": "Late Night Drive", "song_ids": [3, 1, 10]},
    2: {"id": 2, "name": "Morning Coffee", "song_ids": [2, 12, 11, 7]},
}
_next_id = 3


def view(p):
    """Playlist with full song objects."""
    return {"id": p["id"], "name": p["name"],
            "songs": [SONG_BY_ID[i] for i in p["song_ids"]]}


def get_or_404(pid):
    p = PLAYLISTS.get(pid)
    if not p:
        return None, (jsonify(error="Playlist not found"), 404)
    return p, None


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/songs")
def list_songs():
    q = request.args.get("q", "").lower()
    return jsonify([s for s in SONGS
                    if q in (s["title"] + s["artist"] + s["genre"]).lower()])


@app.get("/api/playlists")
def list_playlists():
    return jsonify([view(p) for p in PLAYLISTS.values()])


@app.post("/api/playlists")
def create_playlist():
    global _next_id
    name = (request.json or {}).get("name", "").strip()
    if not name:
        return jsonify(error="Name is required"), 400
    p = {"id": _next_id, "name": name, "song_ids": []}
    PLAYLISTS[_next_id] = p
    _next_id += 1
    return jsonify(view(p)), 201


@app.put("/api/playlists/<int:pid>")
def rename_playlist(pid):
    p, err = get_or_404(pid)
    if err:
        return err
    name = (request.json or {}).get("name", "").strip()
    if not name:
        return jsonify(error="Name is required"), 400
    p["name"] = name
    return jsonify(view(p))


@app.delete("/api/playlists/<int:pid>")
def delete_playlist(pid):
    p, err = get_or_404(pid)
    if err:
        return err
    del PLAYLISTS[pid]
    return "", 204


@app.post("/api/playlists/<int:pid>/songs")
def add_song(pid):
    p, err = get_or_404(pid)
    if err:
        return err
    sid = (request.json or {}).get("song_id")
    if sid not in SONG_BY_ID:
        return jsonify(error="Song not found"), 404
    if sid in p["song_ids"]:
        return jsonify(error="Song already in playlist"), 409
    p["song_ids"].append(sid)
    return jsonify(view(p)), 201


@app.delete("/api/playlists/<int:pid>/songs/<int:sid>")
def remove_song(pid, sid):
    p, err = get_or_404(pid)
    if err:
        return err
    if sid in p["song_ids"]:
        p["song_ids"].remove(sid)
    return jsonify(view(p))


@app.put("/api/playlists/<int:pid>/songs")
def reorder(pid):
    """Body: {"song_ids": [3, 1, 10]} - new order for the playlist."""
    p, err = get_or_404(pid)
    if err:
        return err
    ids = (request.json or {}).get("song_ids", [])
    if sorted(ids) != sorted(p["song_ids"]):
        return jsonify(error="song_ids must match current songs"), 400
    p["song_ids"] = ids
    return jsonify(view(p))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
