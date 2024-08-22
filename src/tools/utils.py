import os, re

def get_rootdir() -> str:
    cwd = os.path.abspath(os.getcwd())
    try:
        end = re.search(r'src', cwd).start()
        rootdir = cwd[:end]
    except:
        end = re.search(r'scrapestaurant', cwd).end()
        rootdir = cwd[:end]

    return rootdir