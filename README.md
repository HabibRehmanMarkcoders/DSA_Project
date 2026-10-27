# Pulse — Music Playlist Manager (Array DSA)

A Python Streamlit app for managing playlists.  
**DSA concept:** simple **array** (Python `list`) — add with `append`, delete with `pop(index)`.

| File | What it is | For presentation |
|---|---|---|
| `DSA_Concept.py` | Array logic + easy English comments | **Show this to your teacher** |
| `UI.py` | Buttons and screens (Streamlit) | Skip if you only need DSA |
| `app.py` | Short pointer / backup entry | Not needed for explaining DSA |

---

## What you need

- **Python 3.10 or newer** (3.12 recommended)
- **pip** (comes with Python)
- An internet connection (to install packages and stream demo MP3s)

---

## Step 1 — Install Python

### Windows

1. Go to: https://www.python.org/downloads/
2. Download the latest **Python 3** installer.
3. Run the installer.
4. **Important:** check the box **“Add python.exe to PATH”**.
5. Click **Install Now**.
6. When it finishes, open a new **Command Prompt** or **PowerShell** and check:

```bash
python --version
```

You should see something like `Python 3.12.x`.

Also check that pip works:

```bash
pip --version
```

If `python` is not recognized, try:

```bash
py --version
```

and use `py` instead of `python` in later commands.

### macOS

```bash
brew install python
python3 --version
pip3 --version
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

---

## Step 2 — Open the project folder

**Windows example:**

```bash
cd C:\Users\USER\OneDrive\Desktop\dsa
```

**macOS / Linux example:**

```bash
cd ~/Desktop/dsa
```

Confirm you see `DSA_Concept.py`, `UI.py`, and `requirements.txt`:

```bash
dir
```

(On macOS / Linux use `ls` instead of `dir`.)

---

## Step 3 — (Recommended) Create a virtual environment

**Windows:**

```bash
python -m venv venv
```

Activate it:

```bash
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

If PowerShell blocks activation:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 4 — Install packages

**Windows:**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

---

## Step 5 — Run the app

```bash
streamlit run UI.py
```

The app opens in your browser (usually http://localhost:8501).

### DSA-only demo (no UI — good for practice)

```bash
python DSA_Concept.py
```

### Stop the app

Press `Ctrl + C` in the terminal.

### Deactivate the virtual environment (optional)

```bash
deactivate
```

---

## Features (mapped to DSA)

- Create playlist → `append` to playlists array
- Delete playlist → `pop(index)` from playlists array
- Add song → `append` to playlist songs array
- Remove song → `pop(index)` from playlist songs array
- Move up / down → swap two indexes in the array
- Search library → loop over the library array

Data is in memory for the session (resets when you stop/restart the app).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Reinstall Python and enable **Add to PATH**, or use `py` |
| `pip` not found | `python -m ensurepip --upgrade` then `python -m pip install --upgrade pip` |
| `streamlit` not found | Activate venv, then `pip install -r requirements.txt` |
| PowerShell activation error | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Port already in use | `streamlit run UI.py --server.port 8502` |
| Audio does not play | Check your internet connection |

---

## All commands combined (Windows)

```bash
cd C:\Users\USER\OneDrive\Desktop\dsa
python --version
pip --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run UI.py
```

**Command Prompt** activation line (instead of `Activate.ps1`):

```bash
venv\Scripts\activate.bat
```

---

## All commands combined (macOS / Linux)

```bash
cd ~/Desktop/dsa
python3 --version
pip3 --version
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
streamlit run UI.py
```
