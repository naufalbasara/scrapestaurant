import pandas as pd, os, re
from tools.utils import get_rootdir
from datetime import datetime

if __name__ == "__main__":
    rootdir = get_rootdir()

    try:
        df = pd.read_csv(os.path.join(rootdir, 'data/scraping_result.csv'))
        df = df.drop(columns='Unnamed: 0')
        df = df.drop_duplicates()
        print(df.info())
    except:
        pass

    df['District'] = df['Category'].str.split('|').str[:-1]
    df['District'] = df['District'].str.join(' ').str.strip()
    df['Category'] = df['Category'].str.split('|').str[-1]

    df['Rating'] = df['Rating'].apply(lambda x: float(x.split()[0])).astype(float)
    df['Restaurant Detail Link'] = df['Restaurant Detail Link'].apply(lambda x: "https://pergikuliner.com" + x)

    df = df.rename(columns={'Price': 'Price Range'})

    print('\nSaving data locally in excel...')
    try:
        df.to_excel(os.path.join(rootdir, f'data/transform_result-{datetime.now().date().__str__()}.xlsx'))
        print('\tData saved in local (excel) successfully...')
    except:
        print('Data failed to saved in excel.')
        print('\nSaving data locally in csv...')
        df.to_csv(os.path.join(rootdir, f'data/transform_result-{datetime.now().date().__str__()}.csv'))
        
        print('\tData saved in local (csv) successfully...')