# Music Playlist Manager — Project Guide

**Print / Word tip:** Open this file in Microsoft Word (or copy all text into Word). Set the font size to **20**. With normal margins, this document is about **6 to 7 pages**.

---

## 1. Introduction (simple English)

This project is a small music playlist manager. The main learning goal is a **Data Structures and Algorithms (DSA)** idea called an **array**.

In Python, an array is made with a **list**. A list stores items in a line, one after another. Each place in the line has a number called an **index**. The first item is at index `0`. The second item is at index `1`. The third item is at index `2`. And so on.

Our music app uses arrays in two ways:

1. An array of **songs** inside one playlist.
2. An array of **playlists** inside the whole app.

When a user adds a song, we use **append**. Append means: put the new item at the **end** of the array. When a user deletes a song, we use **pop(index)**. Pop means: remove the item at that **position** and close the gap.

The file that holds this logic is **`DSA_Concept.py`**. This is the most important file for your teacher and for your presentation. The other files only help the screen look nice or help you install and run the project.

This README explains the DSA file in simple words. It also gives a short summary of every other file and how it is used.

---

## 2. Project idea in one sentence

We store playlist songs in an array, add with append, delete with pop by index, and move songs by swapping two places.

---

## 3. Main DSA concepts used in `DSA_Concept.py`

### 3.1 What is an array here?

An array is a row of boxes:

```text
Index:   0        1        2
Song:  SongA    SongB    SongC
```

- To **read** SongB, we use index `1`.
- To **add** SongD, we append it at the end. Now the array has indexes `0, 1, 2, 3`.
- To **delete** SongB, we pop index `1`. SongC moves left into index `1`.

This is the same idea your teacher asked for:

- add music → `array.append(...)`
- delete music → `array.pop(index)` or remove at that index

### 3.2 Why not a stack?

A **stack** only adds and removes from one end (push and pop from the top). Our teacher also wants delete by **index**, and we need move up / move down. That is **array** behavior, not stack behavior. So this project uses a simple array (Python list).

### 3.3 Important words

| Word | Meaning in this project |
|---|---|
| Array / list | A line of items stored in order |
| Index | Position number starting from 0 |
| Append | Add at the end |
| Pop(index) | Remove the item at that position |
| Swap | Exchange two items using a temp variable |
| Loop | Visit items one by one (we use `while`) |
| Dictionary | One song’s data: id, title, artist, genre, url |

---

## 4. Full logic of `DSA_Concept.py` (main part)

This section explains the whole DSA file from top to bottom in easy English.

### 4.1 Part 1 — Making one song and the song library

#### Function: `make_one_song`

This function builds **one song**. A song is a dictionary (a small box of fields):

- `id` — a number that identifies the song
- `title` — song name
- `artist` — singer or band
- `genre` — music type
- `url` — internet link to play a demo MP3

We build it step by step:

1. Make an empty dictionary: `song = {}`
2. Fill each field one by one
3. Return the song

This is easy to explain: “A song is just data stored in a dictionary.”

#### Function: `make_song_library`

This function builds the **full library array**.

1. Start with an empty list: `library = []`
2. Call `make_one_song` for each sample track
3. Use **`library.append(...)`** every time

So the library itself is an array. At the end we have 12 songs. Index `0` is the first song. Index `11` is the last song.

**DSA point to say:** “We create the library by appending songs into an empty array.”

---

### 4.2 Part 2 — Class `PlaylistArray` (one playlist)

One playlist is one object. Inside it, the important field is:

```text
self.songs = []
```

That empty list **is the array** for that playlist.

#### `__init__(self, name)`

- Saves the playlist name
- Creates an empty songs array

#### `size(self)`

- Returns how many songs are in the array
- Uses `len(self.songs)`

#### `get_all(self)`

- Returns the full songs array
- Used when the UI wants to show every song

#### `get_at(self, index)`

- Reads one song at a given index
- First checks if the index is valid
- If index is too small or too big, returns `None`
- If index is ok, returns `self.songs[index]`

**DSA point:** Reading from an array by index is fast and direct.

#### `add_song(self, song)` — APPEND

This is the main **Create** operation for songs.

Logic:

1. Start `i = 0`
2. Loop with `while` through the songs array
3. If the same song `id` is already there, return `False` (do not add twice)
4. If not found, call **`self.songs.append(song)`**
5. Return `True`

**What to tell the teacher:**  
“To add music, we use array append. Append puts the song at the end of the playlist array.”

#### `remove_song_at(self, index)` — POP BY INDEX

This is the main **Delete** operation for songs.

Logic:

1. Find the last valid index: `len(self.songs) - 1`
2. If index is invalid, return `None`
3. If index is valid, call **`self.songs.pop(index)`**
4. Return the removed song

After pop, every song after that index moves one step left. That is normal array delete behavior.

**What to tell the teacher:**  
“To delete music, we remove by index using pop. We do not need the song name. We only need the position number.”

#### `has_song(self, song_id)`

- Loops through the array
- Returns `True` if that song id is already inside
- Used so the UI can show “Added” instead of “Add”

#### `move_up(self, index)` — SWAP

Moves a song one step toward the front.

Logic:

1. If index is `0` or invalid, stop (cannot move up)
2. Let `above = index - 1`
3. Swap using a temp variable:

```text
temp = songs[above]
songs[above] = songs[index]
songs[index] = temp
```

**What to tell the teacher:**  
“Move up is not append or pop. It is a swap of two indexes in the array.”

#### `move_down(self, index)` — SWAP

Same idea as move up, but with the next index:

1. If already last, stop
2. Let `below = index + 1`
3. Swap with temp

#### `rename(self, new_name)`

- Only changes the playlist name text
- Not an array operation
- Still useful for the app

---

### 4.3 Part 3 — Class `PlaylistManager` (array of playlists)

This class manages the whole app data.

It stores:

- `self.playlists` — array of playlist objects
- `self.library` — array of all available songs
- `self.current_index` — which playlist is selected right now

So we have **array inside array**:

```text
playlists array
   ├── playlist[0].songs array
   ├── playlist[1].songs array
   └── ...
```

#### `__init__(self)`

1. Make empty playlists array
2. Build the song library
3. Set current index to `0`
4. Call `make_starter_playlists()` so the app is not empty at start

#### `find_song_by_id(self, song_id)`

- Linear search in the library array
- Start at `i = 0`
- Compare each song id
- Return the song when found
- Return `None` if not found

**DSA point:** This is a simple search loop over an array.

#### `make_starter_playlists(self)`

Creates two ready playlists:

1. **Late Night Drive** — adds songs with ids 3, 1, 10
2. **Morning Coffee** — adds songs with ids 2, 12, 11, 7

For each song id:

1. Find the song in the library
2. Call `add_song` (which uses append)
3. Finally append the playlist object into `self.playlists`

**DSA point:** We append songs into a playlist array, then append that playlist into the playlists array.

#### `create_playlist(self, name)` — APPEND PLAYLIST

1. If name is empty, return `None`
2. Make a new `PlaylistArray(name)` with empty songs list
3. **`self.playlists.append(playlist)`**
4. Set `current_index` to the new last index
5. Return the playlist

**Teacher line:** “Creating a playlist is also append, but on the playlists array.”

#### `delete_playlist(self, index)` — POP PLAYLIST

1. Check index is valid
2. **`self.playlists.pop(index)`**
3. Fix `current_index` so it still points to a real playlist
4. If no playlists left, set `current_index` to `None`

**Teacher line:** “Deleting a playlist uses pop by index on the playlists array.”

#### `rename_playlist(self, index, new_name)`

- Finds playlist at index
- Calls that playlist’s `rename` method

#### `get_current(self)`

- Returns the selected playlist using `self.playlists[self.current_index]`
- Returns `None` if nothing is selected or index is bad

#### `select_playlist(self, index)`

- Sets `current_index` to the chosen index
- This is how the UI switches between playlists

#### `search_library(self, query)`

This searches the library array.

Logic:

1. If query is empty, return the full library
2. Make a new empty result array
3. Loop every song in the library
4. Convert title, artist, genre to lower case
5. If query text is inside any of them, append that song into result
6. Return result

**DSA point:** Search is a loop over an array, and matches are collected with append into a new array.

---

### 4.4 Part 4 — Demo at the bottom (`if __name__ == "__main__"`)

If you run:

```bash
python DSA_Concept.py
```

the file prints a small demo with no UI. It shows:

1. How many playlists exist
2. Songs in the current playlist with their indexes
3. Add one song with append
4. Remove the song at index `0` with pop
5. Print the new size

This is perfect for practice before a viva. You can run it and explain each printed line.

---

## 5. CRUD mapped to DSA operations

| User action | DSA operation in code | Where |
|---|---|---|
| Add song to playlist | `append` | `PlaylistArray.add_song` |
| Remove song | `pop(index)` | `PlaylistArray.remove_song_at` |
| Show songs | read array / loop | `get_all`, `get_at` |
| Move song up/down | swap with temp | `move_up`, `move_down` |
| Create playlist | `append` | `PlaylistManager.create_playlist` |
| Delete playlist | `pop(index)` | `PlaylistManager.delete_playlist` |
| Search songs | loop + append matches | `search_library` |

This table is useful if the teacher asks: “Where is your DSA?”

Answer: “All of it is in `DSA_Concept.py`. The UI only calls these methods.”

---

## 6. How data flows (simple picture)

**Add:** User clicks Add → `UI.py` calls `add_song` → `DSA_Concept.py` does `append` → array grows at the end.

**Delete:** User clicks Remove on index 2 → `UI.py` calls `remove_song_at(2)` → `DSA_Concept.py` does `pop(2)` → array shrinks and later songs shift left.

---

## 7. Summary of other files (what they do and how used)

### 7.1 `UI.py`

**What it is:** The visual screen made with Streamlit.

**What it does:**

- Shows sidebar with playlist names
- Shows create / rename / delete playlist buttons
- Shows songs in the current playlist
- Shows the song library and search box
- Plays audio with `st.audio`

**How it is used:**

- It imports `PlaylistManager` from `DSA_Concept.py`
- When you click a button, it calls DSA methods like `add_song`, `remove_song_at`, `move_up`, `create_playlist`
- It does **not** do the real array append/pop logic itself

**Run command:**

```bash
streamlit run UI.py
```

**For presentation:** You do not need to explain this file in depth if the teacher asks only about DSA.

### 7.2 `app.py`

**What it is:** A short entry / helper file.

**What it does:**

- Tells you that DSA is in `DSA_Concept.py`
- Tells you that UI is in `UI.py`
- Can load the UI if someone still runs `streamlit run app.py`

**How it is used:** Mostly as a pointer. The recommended run command is still `streamlit run UI.py`.

### 7.3 `requirements.txt`

**What it is:** A list of Python packages to install.

**What it does:** Right now it lists Streamlit (the UI library).

**How it is used:**

```bash
pip install -r requirements.txt
```

This installs the tools needed to show the screen. It is not DSA logic.

### 7.4 `README.md` (this file)

**What it is:** Project documentation.

**What it does:** Explains the array concept, the DSA file logic, how to run the project, and what each file is for.

**How it is used:** Read it before presentation. Open it in Word at font size 20 for about 6–7 pages.

---

## 8. How to run the project (short steps)

1. Install Python 3 (Windows: tick **Add to PATH**).
2. Open the project folder in terminal.
3. Install packages: `pip install -r requirements.txt`
4. Run UI: `streamlit run UI.py`
5. Practice DSA only: `python DSA_Concept.py`

**Windows commands together:**

```bash
cd C:\Users\USER\OneDrive\Desktop\dsa
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run UI.py
```

---

## 9. What to say in the presentation (short script)

“Our DSA concept is an array. In Python we use a list. Each playlist has an array called `songs`. To add a song we use append at the end. To delete a song we use pop with an index. To reorder songs we swap two indexes with a temporary variable. We also keep an array of playlists. Create playlist uses append. Delete playlist uses pop by index. All logic is in `DSA_Concept.py`. The UI only calls these functions.”

---

## 10. Final checklist before viva

- Open `DSA_Concept.py` and find `add_song` / `remove_song_at`
- Explain append, pop(index), and swap in one sentence each
- Say why array (not stack): we delete by index and reorder
- Run `python DSA_Concept.py` and explain the printed output
- Remember: `UI.py` only calls DSA methods

---

## 11. Closing summary

This project teaches one clear DSA idea: **the array**.  
`DSA_Concept.py` is the brain (append, pop, loop, swap).  
`UI.py` is only the face. Other files help you install and run.  

If the teacher asks “Where is your DSA?” — answer: **`DSA_Concept.py`**.
