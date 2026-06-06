
# NMG Sprint 01: SEO Command Center /// this is my submission Bhavya Goyal  https://myselfgoyal.vercel.app
Thanks for the pizza and good vibes..... ENJOYED !! 
Hey! This is my submission for the NMG Forge hackathon. 

The goal was to build an autonomous SEO tool. I tried to look at the problem exactly how NMG Technologies handles their real clients—the tool needed to take raw Screaming Frog data and just *work*, making the issues obvious and actionable without any bs.  ,, used all tools locally either by docs or stuff

## What I built
- A 4-agent pipeline (Ingest, Audit, Fix, Report).
- 17 strict Pandas rules to catch SEO issues deterministically.
- A local Ollama AI hook to rewrite trash titles automatically.
- A really sleek HTML dashboard with severity badges (cuz nobody likes reading raw JSON).

## The Autologger Crisis (and how I fixed it)
So, minor heart attack during the build: the starter bundle's hook failed and my `.claude/audit.jsonl` was stuck at 0 bytes. I was definitly not going to fake the timestamps. Instead, I pulled a senior engiener move: I dug into the global `~/.claude/projects/` directory on my Mac, recovered the massive unedited raw session log, and manually mapped it to `agent-log.md`. Documented the whole save in `DECISIONS.md`. Process points = secured. 🤝

## How to run this thing
Make sure you have Ollama installed and running in the background for the AI fix engine to work!

1. Install dependencies: `pip3 install pandas flask flask-socketio jsonschema`
2. Boot the live dashboard: `python3 mcp/server.py` (Keep this open in tab 1!)
3. In a new terminal tab, run the magic: `python3 run.py sample-export/`

That's it. It'll chew through the CSV and spit out the JSON and CSVs in the `outputs/` folder. 
Open `outputs/report.html` in your browser to see the final client deliverable. 

Built with sweat, terminal hangs :))))))))) 




Uploading some sceenshots 
<img width="1440" height="900" alt="Screenshot 2026-06-06 at 4 58 33 PM" src="https://github.com/user-attachments/assets/d0474a8a-8836-48d1-9085-45b6f4cf9287" />
<img width="1440" height="900" alt="Screenshot 2026-06-06 at 4 58 36 PM" src="https://github.com/user-attachments/assets/8d6b31d3-43b3-4060-8247-f3963eaf7403" />
<img width="1440" height="900" alt="Screenshot 2026-06-06 at 4 58 37 PM" src="https://github.com/user-attachments/assets/7a1bb428-3c91-41d7-a836-75d6f1e33b58" />
<img width="1440" height="900" alt="Screenshot 2026-06-06 at 4 58 47 PM" src="https://github.com/user-attachments/assets/7446df20-38fa-4e9a-b3a6-bed48e42775c" />

<img width="1440" height="900" alt="Screenshot 2026-06-06 at 4 58 53 PM" src="https://github.com/user-attachments/assets/b5e6dc53-3bad-4036-a065-3fb72f3c7ba7" />
