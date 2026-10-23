# Pulse — Music Playlist Manager

A Python Streamlit app for managing playlists and playing demo songs. All CRUD (create, read, update, delete) runs in Python — no separate backend or JavaScript.

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
# Option A — Homebrew
brew install python

# Then check
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

In Command Prompt / PowerShell / Terminal, go to the project directory.

**Windows example:**

```bash
cd C:\Users\USER\OneDrive\Desktop\dsa
```

**macOS / Linux example:**

```bash
cd ~/Desktop/dsa
```

Confirm you see `app.py` and `requirements.txt`:

```bash
dir
```

(On macOS / Linux use `ls` instead of `dir`.)

---

## Step 3 — (Recommended) Create a virtual environment

This keeps project packages separate from your system Python.

**Windows (Command Prompt / PowerShell):**

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

If PowerShell blocks activation, run this once, then try again:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

When the venv is active, your prompt usually starts with `(venv)`.

---

## Step 4 — Install packages

Install everything listed in `requirements.txt` (Streamlit and its dependencies):

**Windows (with `python` / `pip`):**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Wait until installation finishes with no errors.

---

## Step 5 — Run the app

```bash
streamlit run app.py
```

Streamlit will start a local server and open the app in your browser (usually at http://localhost:8501).

If the browser does not open by itself, copy the URL from the terminal and paste it into Chrome / Edge / Firefox.

### Stop the app

In the terminal, press:

```text
Ctrl + C
```

### Deactivate the virtual environment (optional)

```bash
deactivate
```

---

## Features

- Create, rename, and delete playlists
- Search the song library and add tracks
- Reorder songs (up / down) and remove them
- Play a track or play all (via Streamlit audio player)

Data is stored in memory for the browser session (resets when you stop/restart the app).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Reinstall Python and enable **Add to PATH**, or use `py` |
| `pip` not found | Run `python -m ensurepip --upgrade` then `python -m pip install --upgrade pip` |
| `streamlit` not found | Make sure the venv is activated, then run `pip install -r requirements.txt` again |
| PowerShell activation error | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Audio does not play | Check your internet connection (demo MP3s are loaded from the web) |

---

## All commands combined (Windows)

Copy and run these in order from **PowerShell** or **Command Prompt**.  
Adjust the `cd` path if your project folder is somewhere else.

```bash
cd C:\Users\USER\OneDrive\Desktop\dsa
python --version
pip --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
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
streamlit run app.py
```
