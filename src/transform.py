import pandas as pd, os, re, time
from tools.utils import get_rootdir
from datetime import datetime

if __name__ == "__main__":
    time_start = time.time()
    rootdir = get_rootdir()

    try:
        df = pd.read_csv(os.path.join(rootdir, 'data/scraping_result.csv'))
        df = df.drop(columns='Unnamed: 0')
        df = df.reset_index().set_index('index')
        df = df.drop_duplicates()
        print(df.info())
    except:
        pass
    
    # preprocess district and category columns
    df['District'] = df['Category'].str.split('|').str[:-1]
    df['District'] = df['District'].str.join(' ').str.strip()
    df['Category'] = df['Category'].str.split('|').str[-1]
    df['Category'] = df['Category'].str.strip()

    # preprocess missing value in category column
    copy_to_fill = df[(df['District'].isna()) | (df['District'] == '')].index.tolist()
    df.loc[copy_to_fill, 'District'] = df.loc[copy_to_fill]['Category']
    df.loc[copy_to_fill, 'Category'] = 'Not identified yet'

    # preprocess rating and restaurant detail link
    df['Rating'] = df['Rating'].apply(lambda x: float(x.split()[0])).astype(float)
    df['Restaurant Detail Link'] = df['Restaurant Detail Link'].apply(lambda x: "https://pergikuliner.com" + x)

    df = df.rename(columns={'Price': 'Price Range'})

    print('\nSaving data locally in excel...')
    try:
        df.to_excel(os.path.join(rootdir, f'data/transform_result-{datetime.now().date().__str__()}.xlsx'))
        print('\tData saved in local (excel) successfully...')
    except Exception as error:
        print('Data failed to saved in excel.')
        print('\nSaving data locally in csv...')
        df.to_csv(os.path.join(rootdir, f'data/transform_result-{datetime.now().date().__str__()}.csv'))
        
        print('\tData saved in local (csv) successfully...')

    print(f"Data transformation takes up to {time.time() - time_start}s")