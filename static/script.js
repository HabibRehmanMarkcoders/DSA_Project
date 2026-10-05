const $ = (id) => document.getElementById(id);
const state = { playlists: [], songs: [], currentId: null, playingId: null };

async function api(path, method = "GET", body) {
  const res = await fetch("/api" + path, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = res.status === 204 ? null : await res.json();
  if (!res.ok) { toast(data?.error || "Something went wrong"); throw new Error(data?.error); }
  return data;
}

function toast(msg) {
  const t = $("toast"); t.textContent = msg; t.classList.add("show");
  clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove("show"), 2200);
}

const current = () => state.playlists.find((p) => p.id === state.currentId);
const coverStyle = (id) =>
  `background:linear-gradient(145deg,hsl(${id * 47 % 360} 52% 48%),hsl(${(id * 47 + 55) % 360} 45% 28%))`;
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const icons = {
  play: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>`,
  up: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>`,
  down: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>`,
  remove: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>`,
  add: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>`,
  check: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12l5 5L19 7"/></svg>`,
};

function songRow(s, buttons) {
  return `<li data-id="${s.id}" class="${s.id === state.playingId ? "playing" : ""}">
    <div class="cover" style="${coverStyle(s.id)}"></div>
    <div class="info"><b>${esc(s.title)}</b><span>${esc(s.artist)}</span></div>
    <span class="tag">${esc(s.genre)}</span>
    <div class="song-actions">${buttons}</div></li>`;
}

function renderPlaylists() {
  $("playlists").innerHTML = state.playlists.map((p) =>
    `<li data-id="${p.id}" class="${p.id === state.currentId ? "active" : ""}">
       <span>${esc(p.name)}</span><small>${p.songs.length}</small></li>`).join("")
    || `<li class="empty-side">No playlists yet</li>`;
}

function renderCurrent() {
  const p = current();
  if (!p) {
    $("current").innerHTML = `<div class="empty"><strong>Start your first playlist</strong>Create one from the sidebar to begin collecting tracks.</div>`;
    return;
  }
  const rows = p.songs.map((s, i) => songRow(s, `
    <button class="icon" data-act="play" data-id="${s.id}" title="Play">${icons.play} Play</button>
    <button class="icon" data-act="up" data-id="${s.id}" ${i === 0 ? "disabled" : ""} title="Move up">${icons.up}</button>
    <button class="icon" data-act="down" data-id="${s.id}" ${i === p.songs.length - 1 ? "disabled" : ""} title="Move down">${icons.down}</button>
    <button class="icon" data-act="remove" data-id="${s.id}" title="Remove">${icons.remove}</button>`)).join("");
  $("current").innerHTML = `
    <div class="row">
      <div>
        <h2>${esc(p.name)}</h2>
        <p class="section-sub">${p.songs.length} track${p.songs.length === 1 ? "" : "s"} in this playlist</p>
      </div>
      <div class="actions">
        <button data-act="playall">${icons.play} Play all</button>
        <button class="ghost" data-act="rename">Rename</button>
        <button class="danger" data-act="delete">Delete</button>
      </div>
    </div>
    <ul class="songs">${rows || `<li class="empty"><strong>This playlist is empty</strong>Add songs from the library below.</li>`}</ul>`;
}

function renderLibrary() {
  const p = current();
  $("library").innerHTML = state.songs.map((s) => {
    const inList = p?.songs.some((x) => x.id === s.id);
    return songRow(s, `
      <button class="icon" data-act="play" data-id="${s.id}">${icons.play} Play</button>
      <button class="${inList ? "primary-soft" : ""}" data-act="add" data-id="${s.id}" ${!p || inList ? "disabled" : ""}>
        ${inList ? icons.check + " Added" : icons.add + " Add"}
      </button>`);
  }).join("") || `<li class="empty"><strong>No matches</strong>Try another title, artist, or genre.</li>`;
}

const render = () => { renderPlaylists(); renderCurrent(); renderLibrary(); };

function play(id) {
  const all = [...state.songs, ...state.playlists.flatMap((p) => p.songs)];
  const s = all.find((x) => x.id === id);
  if (!s) return;
  state.playingId = id;
  $("audio").src = s.url;
  $("audio").play().catch(() => {});
  $("now").textContent = s.title;
  $("now-sub").textContent = s.artist + " · " + s.genre;
  const art = $("now-art");
  art.style.background = coverStyle(s.id);
  art.classList.add("live");
  render();
}

function replacePlaylist(updated) {
  const i = state.playlists.findIndex((p) => p.id === updated.id);
  state.playlists[i] = updated;
}

async function move(id, dir) {
  const ids = current().songs.map((s) => s.id);
  const i = ids.indexOf(id), j = i + dir;
  [ids[i], ids[j]] = [ids[j], ids[i]];
  replacePlaylist(await api(`/playlists/${state.currentId}/songs`, "PUT", { song_ids: ids }));
}

document.addEventListener("click", async (e) => {
  const li = e.target.closest("#playlists li[data-id]");
  if (li) { state.currentId = +li.dataset.id; return render(); }

  const btn = e.target.closest("button[data-act]");
  if (!btn) return;
  const id = +btn.dataset.id, pid = state.currentId;
  try {
    switch (btn.dataset.act) {
      case "play": return play(id);
      case "playall": { const first = current().songs[0]; return first ? play(first.id) : toast("Playlist is empty"); }
      case "add": replacePlaylist(await api(`/playlists/${pid}/songs`, "POST", { song_id: id })); toast("Added to playlist"); break;
      case "remove": replacePlaylist(await api(`/playlists/${pid}/songs/${id}`, "DELETE")); toast("Removed"); break;
      case "up": await move(id, -1); break;
      case "down": await move(id, 1); break;
      case "rename": {
        const name = prompt("Rename playlist", current().name);
        if (name?.trim()) replacePlaylist(await api(`/playlists/${pid}`, "PUT", { name }));
        break;
      }
      case "delete":
        if (!confirm(`Delete "${current().name}"?`)) return;
        await api(`/playlists/${pid}`, "DELETE");
        state.playlists = state.playlists.filter((p) => p.id !== pid);
        state.currentId = state.playlists[0]?.id ?? null;
        toast("Playlist deleted");
        break;
    }
    render();
  } catch { /* toast already shown */ }
});

$("new-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const p = await api("/playlists", "POST", { name: $("new-name").value });
    state.playlists.push(p); state.currentId = p.id; $("new-name").value = ""; render();
  } catch {}
});

$("search").addEventListener("input", async (e) => {
  state.songs = await api("/songs?q=" + encodeURIComponent(e.target.value));
  renderLibrary();
});

$("audio").addEventListener("ended", () => {
  const songs = current()?.songs || [];
  const i = songs.findIndex((s) => s.id === state.playingId);
  if (i >= 0 && songs[i + 1]) play(songs[i + 1].id);
});

(async function init() {
  [state.songs, state.playlists] = await Promise.all([api("/songs"), api("/playlists")]);
  state.currentId = state.playlists[0]?.id ?? null;
  render();
})();
