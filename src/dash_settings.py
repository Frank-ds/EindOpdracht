"""This module is intended for the dashboard settings"""
# import streamlit as st
# from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import numpy as np
import scipy.integrate as integrate
from datetime import datetime, timedelta
from datetime import datetime, timezone
from settings import settings
import plotly.express as px
import matplotlib.pyplot as plt

import pickle


LOAD_PATH = settings.processed_path

# pickle_files = LOAD_PATH.glob("E214_23*.pkl")
with open(LOAD_PATH / "E214_230128.pkl", "rb") as f:
    df_0128 = pickle.load(f)

with open(LOAD_PATH / "E214_230129.pkl", "rb") as f:
    df_0129 = pickle.load(f)

with open(LOAD_PATH / "E214_230130.pkl", "rb") as f:
    df_0130 = pickle.load(f)

with open(LOAD_PATH / "E214_230131.pkl", "rb") as f:
    df_0131 = pickle.load(f)

with open(LOAD_PATH / "E214_230131.pkl", "rb") as f:
    df_0131 = pickle.load(f)

with open(LOAD_PATH / "E214_A.pkl", "rb") as f:
    df = pickle.load(f)


#
Total_Eng_nrg = np.max(df["engine_used_energy"])
Drive_nrg = np.max(df["drive_energy"])
Hydr_nrg = np.max(df["hydr_energy"])
Idle_nrg = np.max(df["idle_energy"])
Work_nrg = np.max(df["working_energy"])

drive_energy_perc = round(Drive_nrg * 100 / Total_Eng_nrg, 2)
hydr_energy_perc = round(Hydr_nrg * 100 / Total_Eng_nrg, 2)
work_energy_perc = round(Work_nrg * 100 / Total_Eng_nrg, 2)
idle_energy_perc = round(Idle_nrg * 100 / Total_Eng_nrg, 2)


def power_accumulation(df):
    """calculates max energy per function and energy percentage
    returns dictionary"""
    # min_drive_energy = round(np.min(df.drive_energy), 2)
    max_drive_energy = round(np.max(df.drive_energy), 2)
    # drive_energy = max_drive_energy - min_drive_energy
    # min_hydr_energy = round(np.min(df.hydr_energy), 2)
    max_hydr_energy = round(np.max(df.hydr_energy), 2)
    # hydr_energy = max_hydr_energy - min_hydr_energy
    # min_working_energy = round(np.min(df.working_energy), 2)
    max_working_energy = round(np.max(df.working_energy), 2)
    # working_energy = max_working_energy - min_working_energy
    # min_idle_energy = round(np.min(df.idle_energy), 2)
    max_idle_energy = round(np.max(df.idle_energy), 2)
    # idle_energy = max_idle_energy - min_idle_energy
    # min_engine_energy = round(np.min(df.engine_used_energy), 2)
    max_engine_energy = round(np.max(df.engine_used_energy), 2)
    # engine_energy = max_engine_energy - min_engine_energy
    drive_energy_perc = round(max_drive_energy * 100 / max_engine_energy, 2)
    hydr_energy_perc = round(max_hydr_energy * 100 / max_engine_energy, 2)
    work_energy_perc = round(max_working_energy * 100 / max_engine_energy, 2)
    idle_energy_perc = round(max_idle_energy * 100 / max_engine_energy, 2)
    return {
        "drive_energy": max_drive_energy,
        "hydr_energy": max_hydr_energy,
        "working_energy": max_working_energy,
        "idle_energy": max_idle_energy,
        "engine_energy": max_engine_energy,
        "drive_%": drive_energy_perc,
        "hydr_%": hydr_energy_perc,
        "working_%": work_energy_perc,
        "idle_%": idle_energy_perc,
    }


def accumulate_energy(df, input_col):
    """intergration of power gives energy in KWh on range defined in dashboard"""
    nrg = (
        integrate.cumulative_trapezoid(
            df[input_col], (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    nrg_dash = round(np.max(nrg), 2)

    return nrg_dash


SLIDER_LIST = [
    "engine_power",
    "drive_power",
    "hydr_power",
    "idle_power",
    "working_power",
    "engine_used_energy",
    "drive_energy",
    "hydr_energy",
    "idle_energy",
    "working_energy",
    "lat",
    "lon",
    "vehicle_speed",
    "lift_height",
    "truck_state",
]

GPS_LIST = [
    "engine_power",
    "drive_power",
    "hydr_power",
    "idle_power",
    "working_power",
    "lat",
    "lon",
    "vehicle_speed",
    "lift_height",
    "truck_state",
]
