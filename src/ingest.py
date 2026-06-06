import pandas as pd

def load_and_clean_data(file_path):
    # 3. Handle CSV encoding and bad lines
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    
    # 1. Strip column names to avoid extra spaces
    df.columns = df.columns.str.strip()
    
    # Pre-filter: Only rows where Content Type contains "text/html"
    if 'Content Type' in df.columns:
        df = df[df['Content Type'].str.contains('text/html', na=False, case=False)].copy()
        
    # 2. Convert specific columns to numeric, replacing NaNs with 0
    numeric_cols = [
        'Inlinks', 'Word Count', 'Response Time', 
        'Title 1 Length', 'Title 1 Pixel Width', 
        'Meta Description 1 Length'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # Add helper boolean for indexable page definition
    # "indexable page" = Indexability == "Indexable" AND Status Code == 200
    if 'Indexability' in df.columns and 'Status Code' in df.columns:
        # Cast Status Code to numeric just in case, before comparing
        df['Status Code'] = pd.to_numeric(df['Status Code'], errors='coerce')
        df['is_indexable'] = (df['Indexability'] == 'Indexable') & (df['Status Code'] == 200)
    else:
        df['is_indexable'] = False

    return df
