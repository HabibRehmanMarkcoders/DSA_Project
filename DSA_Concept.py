"""
DSA Concept file — Simple ARRAY for music playlists

This is the file your teacher will care about.
We store songs in a Python list. A list works like an array.

Main ideas you can say in the presentation:
  - Add song   -> array.append(song)     (put at the END)
  - Delete     -> array.pop(index)       (remove at a POSITION)
  - Show all   -> loop over the array
  - Move up/down -> swap two indexes
"""

# Demo MP3 links (free sample music from the internet)
URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{}.mp3"

# Sample songs for the library (title, artist, genre)
# This is also an ARRAY of songs.
SAMPLE_SONGS_RAW = [
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


def make_song_library():
    """Build the song library as a simple array (list)."""
    library = []  # empty array at the start
    # loop: go through each sample song one by one
    for i, (title, artist, genre) in enumerate(SAMPLE_SONGS_RAW):
        song = {
            "id": i + 1,           # unique number for this song
            "title": title,
            "artist": artist,
            "genre": genre,
            "url": URL.format(i + 1),  # link to play the mp3
        }
        # DSA: append adds the song at the END of the array
        library.append(song)
    return library


class PlaylistArray:
    """
    One playlist = one ARRAY of songs.

    Think of self.songs like boxes in a row:
      index 0 | index 1 | index 2 | ...
    """

    def __init__(self, name):
        self.name = name
        # This list IS our array. It stores songs in order.
        self.songs = []

    def size(self):
        # How many songs are in the array right now
        return len(self.songs)

    def get_all(self):
        # DSA: return the full array so UI can show it
        return self.songs

    def get_at(self, index):
        # DSA: read the song at this index (position)
        if 0 <= index < len(self.songs):
            return self.songs[index]
        return None

    def add_song(self, song):
        """Add a song to the END of the playlist array."""
        # Do not add the same song twice
        for s in self.songs:
            if s["id"] == song["id"]:
                return False  # already in the array
        # DSA: append adds the song at the END of the array
        self.songs.append(song)
        return True

    def remove_song_at(self, index):
        """Delete the song at this index (position) from the array."""
        # Check that the index is valid (inside the array)
        if 0 <= index < len(self.songs):
            # DSA: pop(index) removes the item at that position
            # and returns the removed song
            return self.songs.pop(index)
        return None

    def has_song(self, song_id):
        # Check if this song id is already in our array
        for s in self.songs:
            if s["id"] == song_id:
                return True
        return False

    def move_up(self, index):
        """Move song one step UP (swap with the song above)."""
        # Cannot move up if it is already the first song (index 0)
        if index <= 0 or index >= len(self.songs):
            return False
        # DSA: swap two places in the array
        above = index - 1
        self.songs[above], self.songs[index] = self.songs[index], self.songs[above]
        return True

    def move_down(self, index):
        """Move song one step DOWN (swap with the song below)."""
        # Cannot move down if it is already the last song
        if index < 0 or index >= len(self.songs) - 1:
            return False
        # DSA: swap two places in the array
        below = index + 1
        self.songs[below], self.songs[index] = self.songs[index], self.songs[below]
        return True

    def rename(self, new_name):
        # Change the playlist name (not an array operation, just a label)
        new_name = (new_name or "").strip()
        if not new_name:
            return False
        self.name = new_name
        return True


class PlaylistManager:
    """
    Manager holds an ARRAY of playlists.

    playlists = [ PlaylistArray("A"), PlaylistArray("B"), ... ]
    """

    def __init__(self):
        # ARRAY of all playlists
        self.playlists = []
        # Song library (ARRAY of all available songs)
        self.library = make_song_library()
        # Which playlist index is selected in the UI (0, 1, 2, ...)
        self.current_index = 0
        # Put two starter playlists in the array so the app is not empty
        self._make_starter_playlists()

    def _find_song_by_id(self, song_id):
        # Search the library array for one song by id
        for song in self.library:
            if song["id"] == song_id:
                return song
        return None

    def _make_starter_playlists(self):
        # Create first playlist and append some songs into its array
        late_night = PlaylistArray("Late Night Drive")
        for song_id in [3, 1, 10]:
            song = self._find_song_by_id(song_id)
            if song:
                late_night.add_song(song)
        # DSA: append this playlist to the playlists array
        self.playlists.append(late_night)

        # Create second playlist
        morning = PlaylistArray("Morning Coffee")
        for song_id in [2, 12, 11, 7]:
            song = self._find_song_by_id(song_id)
            if song:
                morning.add_song(song)
        # DSA: append this playlist to the playlists array
        self.playlists.append(morning)

        # Start by selecting the first playlist (index 0)
        self.current_index = 0

    def create_playlist(self, name):
        """Make a new empty playlist and add it to the playlists array."""
        name = (name or "").strip()
        if not name:
            return None
        playlist = PlaylistArray(name)
        # DSA: append adds the new playlist at the END of the array
        self.playlists.append(playlist)
        # Select the new playlist (it is now the last index)
        self.current_index = len(self.playlists) - 1
        return playlist

    def delete_playlist(self, index):
        """Remove one playlist from the playlists array by index."""
        if 0 <= index < len(self.playlists):
            # DSA: pop(index) removes that playlist from the array
            removed = self.playlists.pop(index)
            # After delete, pick a safe current index
            if len(self.playlists) == 0:
                self.current_index = None
            elif self.current_index is None or self.current_index >= len(self.playlists):
                self.current_index = len(self.playlists) - 1
            return removed
        return None

    def rename_playlist(self, index, new_name):
        """Rename the playlist at this index."""
        if 0 <= index < len(self.playlists):
            return self.playlists[index].rename(new_name)
        return False

    def get_current(self):
        """Return the selected playlist object (or None)."""
        if self.current_index is None:
            return None
        if 0 <= self.current_index < len(self.playlists):
            return self.playlists[self.current_index]
        return None

    def select_playlist(self, index):
        """Select which playlist is current (by index in the array)."""
        if 0 <= index < len(self.playlists):
            self.current_index = index
            return True
        return False

    def search_library(self, query):
        """Search the library array by title, artist, or genre."""
        q = (query or "").lower().strip()
        if not q:
            # No search text -> return full library array
            return self.library
        result = []
        # Loop through the library array and keep matches
        for song in self.library:
            text = (song["title"] + song["artist"] + song["genre"]).lower()
            if q in text:
                # DSA: append matching songs into a new result array
                result.append(song)
        return result


# Quick self-test you can run:  python DSA_Concept.py
# This helps you practice explaining without opening the UI.
if __name__ == "__main__":
    print("=== DSA Array Demo (no UI) ===")
    manager = PlaylistManager()
    print("Playlists in array:", len(manager.playlists))

    current = manager.get_current()
    print("Current playlist:", current.name)
    print("Songs in this playlist array:")
    for i, song in enumerate(current.get_all()):
        print(f"  index {i}: {song['title']}")

    print("\nAdd a song with append...")
    extra = manager.library[4]  # Paper Planes
    current.add_song(extra)
    print("After append, size =", current.size())

    print("\nRemove song at index 0 with pop...")
    removed = current.remove_song_at(0)
    print("Removed:", removed["title"] if removed else None)
    print("Size now =", current.size())
    print("Done. Open DSA_Concept.py to explain these methods to your teacher.")
