from settings import settings
import pathlib as Path
import pandas as pd
import pickle
import load_data
import preprocess

DATA_RAW_DIR = settings.data_raw_dir
DATA_LOADED_DIR = settings.loaded_path
COMBI_FILE = preprocess.combi_file_name

load_data.load_input(DATA_RAW_DIR, DATA_LOADED_DIR)

preprocess.merge_pickles(DATA_LOADED_DIR, COMBI_FILE)

preprocess.preprocess()
print("preproces done")

if __name__ == "__main__":
    print("Main done")
