from settings import settings
import pickle
import pandas as pd
import numpy as np
import scipy.integrate as integrate

# import scipy

conv_path = r"c:\users\frank\Documents\DME\Eindopdracht\data\converted"
with open(conv_path + "\E214_230129.pkl", "rb") as f:
    df = pickle.load(f)


def eng_power_calc(act_trq, Nom_fric, eng_speed):
    # Power calculation
    RefTorque = 850
    EngineTorque = (act_trq - Nom_fric) * RefTorque / 100  # engine torque in Nm
    EnginePower = (
        EngineTorque * (eng_speed * 2 * np.pi / 60) / 1000
    )  # engine power in KW
    return EngineTorque, EnginePower


def Power_accum(eng_pwr, time):
    EnginePower = integrate.cumulative_trapezoid(EnginePower, time, initial=0) / 3600


print(np.mean(EnginePower))
