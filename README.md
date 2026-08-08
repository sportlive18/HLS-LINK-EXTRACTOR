
# 🔴 M3U Stream Extractor Pro

> A **single-file Python web app** that fetches any M3U playlist from GitHub (or anywhere), parses every stream URL, and gives you **10+ ways to copy** them — all with a beautiful animated UI. No dependencies. No CORS issues. Just one file.

---

## ✨ What It Does

Paste a GitHub raw M3U URL → Hit **Scan** → Instantly see every stream URL extracted with full metadata (channel name, group, logo, headers). Copy any URL in any format you need.

**No browser CORS errors.** The Python backend fetches the M3U file server-side, so GitHub raw URLs work perfectly.

---

## 🚀 Quick Start

### Requirements
- **Python 3.6+** (built-in modules only — zero dependencies)

### Run It
```bash
# Clone or download this repo
cd m3u-stream-extractor

# Run the single file
python m3u_extractor.py

# Open in browser
http://localhost:8080
```

That's it. No `pip install`. No `npm install`. No config files.

---

## 📱 Run on Android (Termux)

```bash
pkg install python -y
python m3u_extractor.py
# Open http://localhost:8080 in your Android browser
```

Works perfectly on mobile. Background run supported with `nohup`.

---

### The Parser Reads:
- `#EXTINF` → Channel name, group, logo
- `#EXTVLCOPT` → User-Agent, Referer, Cookie
- `#EXTHTTP` → Extra headers (JSON format)
- `http...` → The actual stream URL

---

## 📋 All Copy Options

### Per Channel (5 buttons on every card)
| Button | What It Copies |
|--------|---------------|
| 📋 | Stream URL only |
| 🔗 | URL + all headers (User-Agent, Referer, Cookie, Origin) |
| 🖥️ | Full `curl` command with all headers |
| 📦 | JSON object of the channel |
| ▶️ | Opens stream directly in **VLC** (`vlc://` protocol) |

### Bulk Actions (top toolbar)
| Button | What It Copies |
|--------|---------------|
| 📋 Copy All URLs | Every stream URL, one per line |
| 🔗 Copy All + Headers | Every URL with its headers |
| 📦 Copy as JSON | Full JSON array of all channels |
| 🖥️ Copy as cURL | `curl` commands for every channel |
| 💾 Download M3U | Rebuilds and saves a clean `.m3u` file |

---

## 🎨 UI Features

- **🔍 Live Search** — Filter channels by name, group, or URL instantly
- **📊 Live Stats** — Channel count, group count, URL count
- **🎭 Channel Logos** — Auto-fetches `tvg-logo` or generates initials avatar
- **🏷️ Group Tags** — Color-coded group badges
- **📱 Fully Responsive** — Works on desktop, tablet, and mobile

### Animations (Pure CSS + Vanilla JS)
- ✨ Staggered card entrance (channels slide in one by one)
- ✨ Hover lift with purple accent bar
- ✨ Logo zoom on hover
- ✨ Button pop + green flash when copied
- ✨ Shimmer effect on Scan button
- ✨ Floating orb in empty state
- ✨ Toast notifications slide in from right

---

## 📂 File Structure

```
m3u-stream-extractor/
└── m3u_extractor.py      # ← Everything is in this ONE file
                           #    (Server + HTML + CSS + JS embedded)
```

No `package.json`. No `requirements.txt`. No `node_modules`. Just **one Python file**.

---

## 🔧 How the Code Works

### Backend (Python ~50 lines)
```python
# Built-in HTTP server on port 8080
# /api/fetch?url=...  → fetches M3U server-side (bypasses CORS)
# /                   → serves the embedded HTML page
```

### Frontend (Embedded HTML/CSS/JS)
```
HTML  → Single-page app with input, stats, toolbar, channel list
CSS   → 400+ lines of pure CSS animations, gradients, responsive design
JS    → M3U parser, 10 copy functions, search filter, toast system
```

### The M3U Parser (Vanilla JS)
```javascript
// Reads line by line:
#EXTINF:-1 tvg-name="STAR SPORTS" group-title="Sports" tvg-logo="...", STAR SPORTS
#EXTVLCOPT:http-user-agent=Hotstar
#EXTVLCOPT:http-referrer=https://www.hotstar.com/
https://jcevents.hotstar.com/.../playlist.m3u8

// Extracts → name, group, logo, url, headers object
```

---


## 🛠️ Customization

### Change Port
```python
# In m3u_extractor.py, change this line:
PORT = 8080   # ← Change to any port you want
```

## ⚠️ Notes

- **VLC button** requires VLC media player installed with the `vlc://` protocol handler
- **Clipboard** requires HTTPS or localhost context (works fine on `localhost:8080`)
- **GitHub URLs** must be **raw** URLs (e.g., `raw.githubusercontent.com/...`)

---

## 📜 License

MIT — Free to use, modify, and distribute.

---

## 🙌 Credits

Built with ❤️ using only **Python built-in modules** + **vanilla JavaScript**. No frameworks. No build step. No dependencies.

**Star ⭐ this repo if you find it useful!**
```

---


