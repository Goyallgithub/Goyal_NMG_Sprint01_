# Project Memory & Rules
- **Goal**: Build an autonomous SEO Command Center plugin that ingests Screaming Frog CSVs, detects issues via strict rules, and fixes titles using a local LLM.
- **Rule 1**: NEVER use AI for detection. Pure pandas only.
- **Rule 2**: 55 points rely on exact string matches for `type` and `severity` in the JSON output schema.
- **Gotchas**: Column names in CSV often have trailing spaces (fixed in `ingest.py` with `.str.strip()`). The local AI sometimes adds quotes to its responses (fixed with `.replace('"', '')`).
