from settings import settings
import Categorize
import Power_split
import pickle
import pandas as pd
import numpy as np
import scipy.integrate as integrate
import os
from datetime import datetime
from pathlib import Path

PROCESSED_PATH = settings.processed_path
LOADED_PATH = settings.loaded_path
combi_file_name = LOADED_PATH.joinpath("E214_A.pkl")

REF_TORQUE = settings.REF_TORQUE  # cummin spec sheet  QSB 6.7 tier 4f
PISTON_DIAM_CM = settings.PISTON_DIAM_CM
PISTON_AREA = settings.PISTON_AREA_CM2


def seconds(df):
    """Make a second series to integrate on"""
    df["seconds"] = np.arange(0, len(df.index), 1)
    return df


def engine_power(df):
    """returns engine power calculated from torque and speed"""
    df["engine_torque"] = (
        (df.engine_actual_torq - df.NomFrictionPercTorq) * REF_TORQUE / 100
    )
    df["engine_power"] = df.engine_torque * (df.engine_speed * 2 * np.pi / 60) / 1000
    return df


# Power accumulation
def engine_energy(df):
    """intergration of engine power gives energy in KWh"""
    df["engine_used_energy"] = (
        integrate.cumulative_trapezoid(df.engine_power, df.seconds, initial=0) / 3600
    )
    return df


def lift_load(df):
    """load on the forks in Tons"""
    df["lifted_load"] = 10 * df.lift_pressure_raw * PISTON_AREA / 10000  # in Tons
    return df


# drop values when category is has no state and enginespeed is 0
def drop_lines_wo_state(df):
    df = df.drop(df[df.truck_state == "drop"].index)
    return df


def accel_rates(df):
    """calculate accped and Joystick rate"""
    df["accelp_rate"] = np.gradient(df.accelpedal_pos, df.seconds)
    df["hoist_rate"] = np.gradient(df.hoist_percentage, df.seconds)
    return df


def preprocess():
    """apply all preprocess functions and wriy=te to a pickle file"""
    for file in LOADED_PATH.glob("*"):
        with open(file, "rb") as f:
            df = pickle.load(f)

        df = seconds(df)
        df = engine_power(df)
        df = engine_energy(df)
        df = lift_load(df)
        df = accel_rates(df)
        df = Categorize.hydraulic_active(df)
        df = Categorize.categorize(df)
        df = Power_split.power_split(df)
        df = Power_split.energy_split(df)
        df = drop_lines_wo_state(df)
        write_to_pickle(file, df)


def write_to_pickle(file, df):
    try:
        with open(PROCESSED_PATH / file.name, "wb") as f:
            pickle.dump(df, f)  # write the file to the output directory
            print(f"preprocessed file {file.name} ")

    except:
        print("failed to make a pickle file")


def merge_pickles(dir_path: str, output_file: str) -> None:
    """
    Merge all .pkl files in a directory into a single .pkl file.
    Args:
    dir_path (str): The path to the directory containing the .pkl files.
    output_file (str): The name of the output .pkl file.
    Returns:
    None
    """
    # Convert input arguments to Path objects
    dir_path = Path(dir_path)
    output_file = Path(output_file)

    files = list(dir_path.glob("*.pkl"))
    merged_df = pd.DataFrame()

    for file in files:
        try:
            with open(file, "rb") as pkl_file:
                print(f"Opening {file}...")
                file_df = pd.read_pickle(pkl_file)
        except:
            print(f"Error: Could not load file {file}. Skipping...")
            continue
        if not isinstance(file_df, pd.DataFrame):
            print(f"Error: File {file} does not contain a DataFrame. Skipping...")
            continue
        merged_df = pd.concat([merged_df, file_df], axis=0)

    merged_df = merged_df.sort_index()
    merged_df.to_pickle(output_file)
    print(f"Combined {len(files)} files into {output_file}")
    print(f"Saved merged file to {output_file.resolve()}")


if __name__ == "__main__":
    print("Data loading module not intended as main")
