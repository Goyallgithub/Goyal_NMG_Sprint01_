import pandas as pd
import requests

def call_local_ai(prompt):
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "gemma4:31b-cloud", "prompt": prompt, "stream": False},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('response', '').strip()
    except Exception:
        pass
    return "Premium Quality Services | Fast & Reliable"

def run_fixes(df, issues):
    fixes = {"titles": [], "redirect_map": []}
    
    title_issue_types = ['missing_title', 'title_too_long', 'title_too_short', 'duplicate_title']
    urls_to_fix = []
    for issue in issues:
        if issue['type'] in title_issue_types:
            urls_to_fix.extend(issue['affected_urls'])
            
    urls_to_fix = list(set(urls_to_fix))[:20]
    
    for url in urls_to_fix:
        old_title = ""
        if 'Address' in df.columns and 'Title 1' in df.columns:
            row = df[df['Address'] == url]
            if not row.empty:
                val = row['Title 1'].iloc[0]
                old_title = str(val) if pd.notna(val) else ""

        new_title = ""
        prompt = f"Write an SEO optimized title tag (under 60 characters) for the URL: {url}. Just return the title, no quotes."
        
        for attempt in range(3):
            candidate = call_local_ai(prompt)
            candidate = candidate.replace('"', '').replace("'", "")
            if len(candidate) <= 60:
                new_title = candidate
                break
        
        if not new_title:
            new_title = candidate[:57] + "..."
            
        fixes["titles"].append({"url": url, "old": old_title, "new": new_title})

    for issue in issues:
        if issue['type'] == 'broken_link':
            for url in issue['affected_urls'][:10]:
                fixes["redirect_map"].append({"from": url, "to": "/", "reason": "4xx error -> closest live fallback (root)"})

    return fixes
