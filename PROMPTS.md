# Key Prompts Log
- **System Scaffold**: "Create a plugin.json mapped to a SKILL.md and 4 sub-agents (ingest, audit, fix, report)." -> Worked perfectly to map the MCP architecture.
- **Title Rewriter Loop**: "Write an SEO optimized title tag (under 60 characters) for the URL: {url}. Just return the title, no quotes." -> Had to wrap this in a 3-try retry loop inside `fix_engine.py` because the local LLM occasionally generated titles longer than 60 chars.
- **Dashboard Update Hook**: "Push state payload to localhost:7700/update" -> Integrated into `run.py` after every major function to ensure the Socket.IO dashboard reflected live progress.
