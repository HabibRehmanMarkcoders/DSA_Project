# ============================================================
# DSA Concept — ARRAY (Python list)
# ============================================================
# Say this to your teacher:
#   Add song     = append          (put at the END)
#   Delete song  = pop(index)      (remove at a POSITION)
#   Show songs   = for loop
#   Move song    = swap two places
# ============================================================


# ---------- 1) Song library (array of songs) ----------

def make_one_song(song_id, title, artist, genre):
    # Make one song as a simple dictionary (like a small box of info)
    song = {}
    song["id"] = song_id
    song["title"] = title
    song["artist"] = artist
    song["genre"] = genre
    # Free demo music link from the internet
    song["url"] = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-" + str(song_id) + ".mp3"
    return song


def make_song_library():
    # Start with an EMPTY array
    library = []

    # Add songs one by one using append
    # DSA: append = put item at the END of the array
    library.append(make_one_song(1, "Neon Rain", "Luna Vale", "Synthwave"))
    library.append(make_one_song(2, "Golden Hour", "The Paper Kites", "Indie"))
    library.append(make_one_song(3, "Midnight Drive", "Kora Blue", "Electronic"))
    library.append(make_one_song(4, "Slow Burn", "Andre Cole", "R&B"))
    library.append(make_one_song(5, "Paper Planes", "Mika Rowe", "Pop"))
    library.append(make_one_song(6, "Salt & Static", "Hollow Tide", "Rock"))
    library.append(make_one_song(7, "Velvet Sky", "Nova Reyes", "Chill"))
    library.append(make_one_song(8, "Run Wild", "The Northern Lights", "Alternative"))
    library.append(make_one_song(9, "Afterglow", "Sable", "Dream Pop"))
    library.append(make_one_song(10, "City of Glass", "Echo Harbor", "Electronic"))
    library.append(make_one_song(11, "Blue Monday Sun", "Jonah Frost", "Folk"))
    library.append(make_one_song(12, "Lantern", "Maya Osei", "Acoustic"))

    return library


# ---------- 2) One playlist = one array of songs ----------

class PlaylistArray:

    def __init__(self, name):
        # Save the playlist name
        self.name = name
        # This list IS our array
        # Example: [song0, song1, song2]
        # Indexes:    0      1      2
        self.songs = []

    def size(self):
        # How many songs are in the array
        return len(self.songs)

    def get_all(self):
        # Give back the whole array
        return self.songs

    def get_at(self, index):
        # Read song at this position (index)
        last_index = len(self.songs) - 1

        if index < 0:
            return None
        if index > last_index:
            return None

        return self.songs[index]

    def add_song(self, song):
        # Check if song is already in the array
        i = 0
        while i < len(self.songs):
            old_song = self.songs[i]
            if old_song["id"] == song["id"]:
                # Already there, do not add again
                return False
            i = i + 1

        # DSA: append puts the song at the END
        self.songs.append(song)
        return True

    def remove_song_at(self, index):
        # Delete song at this position
        last_index = len(self.songs) - 1

        if index < 0:
            return None
        if index > last_index:
            return None

        # DSA: pop(index) removes that position from the array
        removed_song = self.songs.pop(index)
        return removed_song

    def has_song(self, song_id):
        # Is this song id already inside the array?
        i = 0
        while i < len(self.songs):
            song = self.songs[i]
            if song["id"] == song_id:
                return True
            i = i + 1
        return False

    def move_up(self, index):
        # Move song one step UP = swap with the song above
        # Cannot move up if index is 0 (already first)
        if index <= 0:
            return False
        if index >= len(self.songs):
            return False

        above = index - 1

        # DSA: swap using a temp variable (easy to explain)
        temp = self.songs[above]
        self.songs[above] = self.songs[index]
        self.songs[index] = temp
        return True

    def move_down(self, index):
        # Move song one step DOWN = swap with the song below
        last_index = len(self.songs) - 1

        if index < 0:
            return False
        if index >= last_index:
            return False

        below = index + 1

        # DSA: swap using a temp variable
        temp = self.songs[below]
        self.songs[below] = self.songs[index]
        self.songs[index] = temp
        return True

    def rename(self, new_name):
        # Change only the name text
        if new_name == None:
            return False

        # Remove spaces at start and end
        new_name = new_name.strip()

        if new_name == "":
            return False

        self.name = new_name
        return True


# ---------- 3) Manager = array of playlists ----------

class PlaylistManager:

    def __init__(self):
        # Array of all playlists
        self.playlists = []

        # Array of all songs we can pick from
        self.library = make_song_library()

        # Which playlist is selected (0 means first playlist)
        self.current_index = 0

        # Make two starter playlists so app is not empty
        self.make_starter_playlists()

    def find_song_by_id(self, song_id):
        # Look through library array one by one
        i = 0
        while i < len(self.library):
            song = self.library[i]
            if song["id"] == song_id:
                return song
            i = i + 1
        return None

    def make_starter_playlists(self):
        # ---- playlist 1 ----
        late_night = PlaylistArray("Late Night Drive")

        song_a = self.find_song_by_id(3)
        song_b = self.find_song_by_id(1)
        song_c = self.find_song_by_id(10)

        if song_a != None:
            late_night.add_song(song_a)
        if song_b != None:
            late_night.add_song(song_b)
        if song_c != None:
            late_night.add_song(song_c)

        # DSA: append playlist to playlists array
        self.playlists.append(late_night)

        # ---- playlist 2 ----
        morning = PlaylistArray("Morning Coffee")

        song_d = self.find_song_by_id(2)
        song_e = self.find_song_by_id(12)
        song_f = self.find_song_by_id(11)
        song_g = self.find_song_by_id(7)

        if song_d != None:
            morning.add_song(song_d)
        if song_e != None:
            morning.add_song(song_e)
        if song_f != None:
            morning.add_song(song_f)
        if song_g != None:
            morning.add_song(song_g)

        # DSA: append playlist to playlists array
        self.playlists.append(morning)

        # Select first playlist
        self.current_index = 0

    def create_playlist(self, name):
        # Make a new empty playlist and put it in the array
        if name == None:
            return None

        name = name.strip()
        if name == "":
            return None

        playlist = PlaylistArray(name)

        # DSA: append = add at the END of playlists array
        self.playlists.append(playlist)

        # New playlist is now the last one
        self.current_index = len(self.playlists) - 1
        return playlist

    def delete_playlist(self, index):
        # Remove one playlist by its index
        last_index = len(self.playlists) - 1

        if index < 0:
            return None
        if index > last_index:
            return None

        # DSA: pop(index) removes that playlist from the array
        removed = self.playlists.pop(index)

        # Fix current_index after delete
        if len(self.playlists) == 0:
            self.current_index = None
        else:
            # If current index is now too big, go to last playlist
            if self.current_index == None:
                self.current_index = len(self.playlists) - 1
            elif self.current_index >= len(self.playlists):
                self.current_index = len(self.playlists) - 1

        return removed

    def rename_playlist(self, index, new_name):
        last_index = len(self.playlists) - 1

        if index < 0:
            return False
        if index > last_index:
            return False

        playlist = self.playlists[index]
        ok = playlist.rename(new_name)
        return ok

    def get_current(self):
        # Return the selected playlist
        if self.current_index == None:
            return None

        last_index = len(self.playlists) - 1
        if self.current_index < 0:
            return None
        if self.current_index > last_index:
            return None

        return self.playlists[self.current_index]

    def select_playlist(self, index):
        # Choose which playlist is current
        last_index = len(self.playlists) - 1

        if index < 0:
            return False
        if index > last_index:
            return False

        self.current_index = index
        return True

    def search_library(self, query):
        # Search songs in the library array
        if query == None:
            return self.library

        query = query.strip()
        query = query.lower()

        # If search box is empty, return full library
        if query == "":
            return self.library

        # Make a new array for matching songs
        result = []

        i = 0
        while i < len(self.library):
            song = self.library[i]
            title = song["title"].lower()
            artist = song["artist"].lower()
            genre = song["genre"].lower()

            # Simple check: is query text inside title or artist or genre?
            found = False
            if query in title:
                found = True
            if query in artist:
                found = True
            if query in genre:
                found = True

            if found == True:
                # DSA: append match into result array
                result.append(song)

            i = i + 1

        return result


# ---------- 4) Small demo (no UI) ----------
# Run:  python DSA_Concept.py

if __name__ == "__main__":
    print("=== DSA Array Demo ===")

    manager = PlaylistManager()
    print("How many playlists:", len(manager.playlists))

    current = manager.get_current()
    print("Current playlist name:", current.name)

    print("Songs in array:")
    i = 0
    while i < current.size():
        song = current.get_at(i)
        print("  index", i, "=", song["title"])
        i = i + 1

    print("Add song with append...")
    extra = manager.library[4]
    current.add_song(extra)
    print("Size after append:", current.size())
    print("Remove song at index 0 with pop...")
    removed = current.remove_song_at(0)
    if removed != None:
        print("Removed song:", removed["title"])
    print("Size now:", current.size())
