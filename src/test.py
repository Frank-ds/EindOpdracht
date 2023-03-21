import pandas as pd
import pickle

conv_path = r"c:\users\frank\Documents\DME\Eindopdracht\data\converted"
with open(conv_path + "\E214_230129_.pkl", "rb") as f:
    df = pickle.load(f)

df.info()
