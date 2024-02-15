import os
import glob


def clean_blitz() -> None:
    try:
        os.remove("app.db")
    except FileNotFoundError:
        pass

    for file in glob.glob("**/versions/*_migratiob.py"):
        if os.path.isfile(file):
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
