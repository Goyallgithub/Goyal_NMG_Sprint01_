# SEO Audit Skill
## Pipeline
1. Ingest: load_and_clean_data() reads internal_all.csv
2. Audit: detect_issues() applies 17 SEO rules via pandas
3. Fix: run_fixes() rewrites bad titles using local AI
4. Report: build_reports() writes report.json and report.html
## Sub-agents
- ingest: responsible for CSV loading and normalization
- audit: responsible for issue detection
- fix: responsible for AI title rewriting
- report: responsible for output generation
