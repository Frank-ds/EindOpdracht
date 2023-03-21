from settings import settings
import pickle
import pandas as pd
import numpy as np

# import scipy

conv_path = r"c:\users\frank\Documents\DME\Eindopdracht\data\converted"
with open(conv_path + "\E214_230129.pkl", "rb") as f:
    df = pickle.load(f)

# Power calculation
RefTorque = 850
df["EngineTorque"] = (
    (df.Engine_Actual_Torq - df.NomFrictionPercTorq) * RefTorque / 100
)  # engine torque in Nm
df["EnginePower"] = (
    df.EngineTorque * (df.Engine_Speed * 2 * np.pi / 60) / 1000
)  # engine power in KW

# # Power accumulation
# df["EnginePower_acc"] = (
# #     integrate.cumulative_trapezoid(df.EnginePower, df.index, initial=0) / 3600)

print(np.mean(df.EnginePower))
