import pandas as pd, os, time
from tools.gsheet_conn import GSheet
from tools.utils import get_rootdir
from datetime import datetime
from termcolor import colored

if __name__ == "__main__":
    time_start = time.time()
    rootdir = get_rootdir()
    date_extract = datetime.now().date() # - timedelta(days=1) # get current date or adjusting the last extracted data
    print(date_extract)
    try:
        print(f"Accessing data transformed in {date_extract}...", end=' ')
        df = pd.read_csv(os.path.join(rootdir, f'data/transform_result-{date_extract}.csv'))
        df = df.drop(columns='index')
        df = df.drop_duplicates()
        print(colored('success.', color='green'))
    except Exception as error:
        print(colored('failed.', color='red'))
        print(f"{datetime.strftime(datetime.now(), format='%D %H:%M:%S')}: {colored('[ERROR]', color='red')} {error}\n")
        raise colored('Failed to load transformation result', color='red')

    try:
        print("Opening sheet connection...", end=' ')
        sheet = GSheet("1zJERAx1aUZqsB34pjs7LkErZ4zS2sWJ475lE4Ot74Kg")
    except Exception as error:
        print(colored('failed.', color='red'))
        print(f"{datetime.strftime(datetime.now(), format='%D %H:%M:%S')}: {colored('[ERROR]', color='red')} {error}\n")
        
    try:
        print("Loading data to corresponding spreadsheet...", end=' ')
        sheet.trunc_ins(f'Load-{date_extract}', df=df)
        print(colored('success.', color='green'))
    except Exception as error:
        print(colored('failed.', color='red'))
        print(f"{datetime.strftime(datetime.now(), format='%D %H:%M:%S')}: {colored('[ERROR]', color='red')} {error}\n")

    print(f"Data load takes up to {time.time() - time_start}s")