import sys
import os
import requests
from src.ingest import load_and_clean_data
from src.detect import detect_issues
from src.fix_engine import run_fixes
from src.report_builder import build_reports

def push_update(stage, urls=0, issues=0, severities=None):
    if severities is None:
        severities = {"High": 0, "Medium": 0, "Low": 0}
    payload = {
        "stage": stage,
        "urls_processed": urls,
        "issues_found": issues,
        "severities": severities
    }
    try:
        # Push to our local MCP dashboard (fails silently if dashboard isn't booted yet)
        requests.post('http://localhost:7700/update', json=payload, timeout=2)
    except Exception:
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <path_to_export_folder>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    csv_path = os.path.join(target_dir, 'internal_all.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        sys.exit(1)

    print(f"🚀 Starting SEO Command Center audit on {csv_path}...")
    push_update("Ingesting data...", 0, 0)
    
    # 1. Ingest
    df = load_and_clean_data(csv_path)
    urls_processed = len(df)
    
    # 2. Detect
    push_update("Detecting issues...", urls_processed, 0)
    issues = detect_issues(df)
    
    total_issues = len(issues)
    high = sum(1 for i in issues if i.get('severity') == 'High')
    medium = sum(1 for i in issues if i.get('severity') == 'Medium')
    low = sum(1 for i in issues if i.get('severity') == 'Low')
    sevs = {"High": high, "Medium": medium, "Low": low}
    
    # 3. Fix
    push_update("Fixing AI titles & routing...", urls_processed, total_issues, sevs)
    fixes = run_fixes(df, issues)
    
    # 4. Report
    push_update("Generating JSON and HTML reports...", urls_processed, total_issues, sevs)
    build_reports(df, issues, fixes)
    
    push_update("Audit Complete!", urls_processed, total_issues, sevs)
    print("✅ Done! Check outputs/report.json and outputs/report.html")

if __name__ == "__main__":
    main()
