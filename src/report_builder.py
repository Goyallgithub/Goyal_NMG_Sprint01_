import json
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
        
    # Write a clean, human-readable report.html
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>SEO Audit Report - {site}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; color: #333; }}
        h1, h2 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .summary {{ background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .High {{ color: #d32f2f; font-weight: bold; }}
        .Medium {{ color: #f57c00; font-weight: bold; }}
        .Low {{ color: #388e3c; font-weight: bold; }}
        li {{ margin-bottom: 10px; line-height: 1.5; }}
    </style>
</head>
<body>
    <h1>SEO Audit Report: {site}</h1>
    <div class="summary">
        <p><strong>URLs Crawled:</strong> {urls_crawled}</p>
        <p><strong>Total Issues:</strong> {len(issues)} 
           (<span class="High">High: {high}</span> | 
            <span class="Medium">Medium: {medium}</span> | 
            <span class="Low">Low: {low}</span>)
        </p>
    </div>
    <h2>Issues Detected</h2>
    <ul>
"""
    for issue in issues:
        html_content += f"        <li><span class=\"{issue['severity']}\">[{issue['severity']}]</span> <strong>{issue['type']}</strong>: {issue['explanation']}</li>\n"
        
    html_content += """    </ul>
</body>
</html>"""
    
    with open('outputs/report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return report_data
