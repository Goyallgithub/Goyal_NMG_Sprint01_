import pandas as pd

def load_and_clean_data(file_path):
    # 3. Handle CSV encoding and bad lines
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    
    # 1. Strip column names to avoid extra spaces
    df.columns = df.columns.str.strip()
    
    # Pre-filter: Only rows where Content Type contains "text/html"
    df_html = df.copy()
    if 'Content Type' in df.columns:
        df_html = df[df['Content Type'].str.contains('text/html', na=False, case=False)].copy()
        
    # 2. Convert specific columns to numeric, replacing NaNs with 0
    numeric_cols = [
        'Inlinks', 'Word Count', 'Response Time', 
        'Title 1 Length', 'Title 1 Pixel Width', 
        'Meta Description 1 Length'
    ]
    for col in numeric_cols:
        if col in df_html.columns:
            df_html[col] = pd.to_numeric(df_html[col], errors='coerce').fillna(0)
            
    # Add helper boolean for indexable page definition
    # "indexable page" = Indexability == "Indexable" AND Status Code == 200
    if 'Indexability' in df_html.columns and 'Status Code' in df_html.columns:
        # Cast Status Code to numeric just in case, before comparing
        df_html['Status Code'] = pd.to_numeric(df_html['Status Code'], errors='coerce')
        df_html['is_indexable'] = (df_html['Indexability'] == 'Indexable') & (df_html['Status Code'] == 200)
    else:
        df_html['is_indexable'] = False

    df_images = df[df['Content Type'].str.contains('image', na=False, case=False)]
    return df_html, df_images
