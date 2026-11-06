# How to transcribe further episodes

Minute-exact links only exist for episodes with a transcript. This is how more are added:

## Option A – free, on your own PC (recommended)
1. Install Python 3.10+ and ffmpeg, then in the repo folder:
   ```
   pip install faster-whisper
   python scripts/transcribe_local.py
   python scripts/fetch_official.py
   python scripts/build_wiki.py
   ```
2. Obsidian updates itself – every topic article gets quotes with minute links.

Single episodes: `python scripts/transcribe_local.py s06e10 x2026-06-24`
With an NVIDIA graphics card the script uses the GPU (about 15× real time with `large-v3-turbo`).

## Option B – official transcripts
Buzzsprout publishes an official transcript for most episodes. `fetch_official.py` downloads them;
the build merges the official wording with the Whisper timestamps, so those transcripts count as
"aligned with the official transcript".

## Add Spotify links
For minute links on Spotify each episode needs its Spotify ID in `data/spotify_ids.json`
(the part after `/episode/` in the Spotify link). Without it the wiki links to the show.

← [[Real Exam English Wiki|Home]]
