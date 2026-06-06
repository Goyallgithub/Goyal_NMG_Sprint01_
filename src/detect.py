import pandas as pd

def detect_issues(df):
    issues = []
    
    # Helper masks
    idx_200 = df['is_indexable'] == True
    any_200 = df['Status Code'] == 200
    
    def add_issue(type_str, severity, urls_series, explanation_template):
        urls = urls_series.dropna().tolist()
        count = len(urls)
        if count > 0:
            issues.append({
                "type": type_str,
                "severity": severity,
                "affected_urls": urls,
                "count": count,
                "explanation": explanation_template.format(count=count)
            })

    # --- 1. Titles ---
    if 'Title 1' in df.columns:
        empty_title_mask = df['Title 1'].isna() | (df['Title 1'].astype(str).str.strip() == '')
        add_issue('missing_title', 'High', df[empty_title_mask & idx_200]['Address'], "{count} indexable pages have no title tag.")

        valid_titles = df[~empty_title_mask & idx_200]
        dup_titles = valid_titles[valid_titles.duplicated(subset=['Title 1'], keep=False)]
        add_issue('duplicate_title', 'High', dup_titles['Address'], "{count} indexable URLs share duplicate titles.")

        long_title_mask = (df['Title 1 Pixel Width'] > 561) | (df['Title 1 Length'] > 60)
        add_issue('title_too_long', 'Medium', df[long_title_mask]['Address'], "{count} pages have titles exceeding length or pixel limits.")

        short_title_mask = (df['Title 1 Length'] < 30) & (~empty_title_mask)
        add_issue('title_too_short', 'Low', df[short_title_mask]['Address'], "{count} pages have titles under 30 characters.")

    # --- 2. Meta Descriptions ---
    if 'Meta Description 1' in df.columns:
        empty_meta_mask = df['Meta Description 1'].isna() | (df['Meta Description 1'].astype(str).str.strip() == '')
        add_issue('missing_meta_description', 'Medium', df[empty_meta_mask & idx_200]['Address'], "{count} indexable pages have no meta description.")

        valid_metas = df[~empty_meta_mask & idx_200]
        dup_metas = valid_metas[valid_metas.duplicated(subset=['Meta Description 1'], keep=False)]
        add_issue('duplicate_meta_description', 'Medium', dup_metas['Address'], "{count} indexable URLs share duplicate meta descriptions.")

        long_meta_mask = df['Meta Description 1 Length'] > 155
        add_issue('meta_description_too_long', 'Low', df[long_meta_mask]['Address'], "{count} pages have meta descriptions > 155 characters.")

    # --- 3. H1 Tags ---
    if 'H1-1' in df.columns:
        empty_h1_mask = df['H1-1'].isna() | (df['H1-1'].astype(str).str.strip() == '')
        add_issue('missing_h1', 'Medium', df[empty_h1_mask & any_200]['Address'], "{count} 200 OK pages are missing an H1 tag.")

        valid_h1s = df[~empty_h1_mask & idx_200]
        dup_h1s = valid_h1s[valid_h1s.duplicated(subset=['H1-1'], keep=False)]
        add_issue('duplicate_h1', 'Low', dup_h1s['Address'], "{count} indexable URLs share duplicate H1 tags.")

    # --- 4. Status Codes & Redirect Chains ---
    add_issue('broken_link', 'High', df[(df['Status Code'] >= 400) & (df['Status Code'] < 500)]['Address'], "{count} pages return 4xx client errors.")
    add_issue('server_error', 'High', df[(df['Status Code'] >= 500) & (df['Status Code'] < 600)]['Address'], "{count} pages return 5xx server errors.")
    
    redirects = df[(df['Status Code'] >= 300) & (df['Status Code'] < 400)]
    add_issue('redirect', 'Medium', redirects['Address'], "{count} URLs are redirecting (3xx).")

    if 'Redirect URL' in df.columns:
        # Build dict {Address: Redirect URL} for all 3xx rows
        redir_dict = dict(zip(redirects['Address'], redirects['Redirect URL']))
        chain_urls = [addr for addr, target in redir_dict.items() if target in redir_dict]
        add_issue('redirect_chain', 'High', pd.Series(chain_urls), "{count} redirecting URLs point to another redirect.")

    # --- 5. Content & Indexability ---
    add_issue('thin_content', 'Low', df[(df['Word Count'] < 200) & idx_200]['Address'], "{count} indexable pages have < 200 words.")
    add_issue('orphan_page', 'Medium', df[(df['Inlinks'] == 0) & idx_200]['Address'], "{count} indexable pages have 0 incoming internal links.")
    
    if 'Indexability' in df.columns:
        non_idx_linked = (df['Indexability'] == 'Non-Indexable') & (df['Inlinks'] > 0)
        add_issue('non_indexable_but_linked', 'Medium', df[non_idx_linked]['Address'], "{count} non-indexable pages receive internal links.")
    
    add_issue('slow_page', 'Low', df[df['Response Time'] > 1.0]['Address'], "{count} pages have a response time > 1.0s.")

    return issues
