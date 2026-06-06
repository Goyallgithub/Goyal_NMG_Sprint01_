import json
import csv
from urllib.parse import urlparse

def build_reports(df, issues, fixes=None, run_meta=None):
    if fixes is None:
        # Default empty fixes structure
        fixes = {"titles": [], "redirect_map": []}
    if run_meta is None:
        # Default meta matching the model you are using
        run_meta = {"model": "gemma4:31b-cloud", "model_calls": 0, "duration_sec": 0}

    # Detect site name from the first valid Address row
    site = "unknown-site.com"
    if not df.empty and 'Address' in df.columns:
        first_url = df['Address'].dropna().iloc[0]
        if isinstance(first_url, str) and first_url.startswith('http'):
            site = urlparse(first_url).netloc

    urls_crawled = len(df)

    # Calculate severity counts
    high = sum(1 for i in issues if i.get('severity') == 'High')
    medium = sum(1 for i in issues if i.get('severity') == 'Medium')
    low = sum(1 for i in issues if i.get('severity') == 'Low')

    # Construct exact JSON schema
    report_data = {
        "site": site,
        "urls_crawled": urls_crawled,
        "summary": {
            "total_issues": len(issues),
            "by_severity": { "High": high, "Medium": medium, "Low": low }
        },
        "issues": issues,
        "fixes": fixes,
        "recommendations": [f"Fix the {high} High-severity issues first."],
        "run_meta": run_meta
    }

    # Write report.json
    with open('outputs/report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)

    # --- PROFESSIONAL HTML GENERATION ---
    severity_map = {"High": 0, "Medium": 1, "Low": 2}
    sorted_issues = sorted(issues, key=lambda x: severity_map.get(x['severity'], 3))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {site}</title>
    <style>
        :root {{
            --sidebar-bg: #0f172a;
            --body-bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --high-color: #ef4444;
            --medium-color: #f59e0b;
            --low-color: #10b981;
            --border-color: #e2e8f0;
        }}
        body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; display: flex; background: var(--body-bg); color: var(--text-main); }}

        /* Sidebar */
        aside {{ width: 260px; background: var(--sidebar-bg); height: 100vh; position: fixed; color: white; padding: 24px; box-sizing: border-box; }}
        aside h1 {{ font-size: 1.25rem; margin-bottom: 32px; line-height: 1.2; }}
        aside nav {{ display: flex; flex-direction: column; gap: 12px; }}
        aside nav a {{ color: #94a3b8; text-decoration: none; font-size: 0.9rem; transition: color 0.2s; }}
        aside nav a:hover {{ color: white; }}

        /* Main Content */
        main {{ margin-left: 260px; padding: 40px; width: 100%; box-sizing: border-box; }}
        .header {{ margin-bottom: 32px; }}
        .header h2 {{ font-size: 2rem; margin: 0; color: var(--text-main); }}
        .header p {{ color: var(--text-muted); margin-top: 8px; }}

        /* Summary Grid */
        .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ background: var(--card-bg); padding: 24px; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .stat-card h3 {{ margin: 0; font-size: 0.875rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; }}
        .stat-card .value {{ font-size: 2rem; font-weight: 700; margin: 8px 0; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; color: white; }}
        .badge-high {{ background: var(--high-color); }}
        .badge-medium {{ background: var(--medium-color); }}
        .badge-low {{ background: var(--low-color); }}

        /* Issues Section */
        .section-title {{ font-size: 1.5rem; margin: 40px 0 20px 0; color: var(--text-main); }}
        .issue-card {{ background: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border-color); margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .issue-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
        .issue-type {{ font-weight: 600; font-size: 1.1rem; color: var(--text-main); }}
        .issue-desc {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 16px; }}

        details {{ font-size: 0.875rem; color: var(--text-muted); border-top: 1px solid var(--border-color); padding-top: 12px; }}
        details summary {{ cursor: pointer; font-weight: 500; outline: none; }}
        .url-list {{ list-style: none; padding: 0; margin: 12px 0 0 0; }}
        .url-list li {{ padding: 4px 0; overflow-wrap: break-word; font-family: monospace; color: #475569; }}

        /* Fixes Section */
        .fix-card {{ background: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 12px; margin-bottom: 12px; }}
        .fix-pair {{ display: flex; justify-content: space-between; font-size: 0.875rem; margin-bottom: 4px; }}
        .fix-old {{ color: #991b1b; text-decoration: line-through; }}
        .fix-new {{ color: #166534; font-weight: 600; }}
    </style>
</head>
<body>
    <aside>
        <h1>SEO Command Center</h1>
        <nav>
            <a href="#summary">Summary</a>
            <a href="#issues">Issue Analysis</a>
            <a href="#fixes">Fixes Applied</a>
        </nav>
    </aside>
    <main>
        <div class="header">
            <h2>Audit Report: {site}</h2>
            <p>Analysis of {urls_crawled} crawled URLs</p>
        </div>

        <div id="summary" class="summary-grid">
            <div class="stat-card">
                <h3>High Severity</h3>
                <div class="value" style="color: var(--high-color)">{high}</div>
                <span class="badge badge-high">Critical</span>
            </div>
            <div class="stat-card">
                <h3>Medium Severity</h3>
                <div class="value" style="color: var(--medium-color)">{medium}</div>
                <span class="badge badge-medium">Warning</span>
            </div>
            <div class="stat-card">
                <h3>Low Severity</h3>
                <div class="value" style="color: var(--low-color)">{low}</div>
                <span class="badge badge-low">Optimization</span>
            </div>
        </div>

        <h3 id="issues" class="section-title">Issues Detected</h3>
"""
    for issue in sorted_issues:
        severity_class = f"badge-{issue['severity'].lower()}"
        urls = issue['affected_urls'][:5]
        url_html = "".join([f"<li>{url}</li>" for url in urls])

        html_content += f"""
        <div class="issue-card">
            <div class="issue-header">
                <span class="badge {severity_class}">{issue['severity']}</span>
                <span class="issue-type">{issue['type'].replace('_', ' ').title()}</span>
            </div>
            <div class="issue-desc">{issue['explanation']}</div>
            <details>
                <summary>View top {len(urls)} affected URLs</summary>
                <ul class="url-list">{url_html}</ul>
            </details>
        </div>
        """

    html_content += '<h3 id="fixes" class="section-title">Fixes Applied</h3>'

    if fixes.get("titles"):
        html_content += '<div class="fix-group"><h4>AI-Optimized Titles</h4>'
        for fix in fixes["titles"]:
            html_content += f"""
            <div class="fix-card">
                <div style="font-weight:600; font-size:0.8rem; margin-bottom:8px; color:#475569;">{fix['url']}</div>
                <div class="fix-pair"><span>Old:</span> <span class="fix-old">{fix['old']}</span></div>
                <div class="fix-pair"><span>New:</span> <span class="fix-new">{fix['new']}</span></div>
            </div>
            """
        html_content += '</div>'

    if fixes.get("redirect_map"):
        html_content += '<div class="fix-group"><h4>Auto-Redirect Map</h4>'
        for red in fixes["redirect_map"]:
            html_content += f"""
            <div class="fix-card">
                <div class="fix-pair"><span>From:</span> <span class="fix-old">{red['from']}</span></div>
                <div class="fix-pair"><span>To:</span> <span class="fix-new">{red['to']}</span></div>
                <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Reason: {red['reason']}</div>
            </div>
            """
        html_content += '</div>'

    if not fixes.get("titles") and not fixes.get("redirect_map"):
        html_content += '<p style="color: var(--text-muted);">No fixes were applied in this run.</p>'

    html_content += """
    </main>
</body>
</html>"""

    with open('outputs/report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Export fixes to CSV
    titles_fixes = fixes.get('titles', [])
    if titles_fixes:
        with open('outputs/fixes_titles.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'old_title', 'new_title'])
            writer.writeheader()
            for fix in titles_fixes:
                writer.writerow({
                    'url': fix.get('url'),
                    'old_title': fix.get('old'),
                    'new_title': fix.get('new')
                })

    redirect_fixes = fixes.get('redirect_map', [])
    if redirect_fixes:
        with open('outputs/redirect_map.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['from_url', 'to_url', 'reason'])
            writer.writeheader()
            for red in redirect_fixes:
                writer.writerow({
                    'from_url': red.get('from'),
                    'to_url': red.get('to'),
                    'reason': red.get('reason')
                })

    return report_data
