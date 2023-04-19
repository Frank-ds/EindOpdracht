from settings import settings
import categorize
import power_split
import merge
import pickle
import pandas as pd
import numpy as np
import scipy.integrate as integrate
import os
from datetime import datetime
from pathlib import Path

PROCESSED_PATH = settings.processed_path
LOADED_PATH = settings.loaded_path
COMBI_FILE_NAME = LOADED_PATH.joinpath("E214_A.pkl")

REF_TORQUE = settings.REF_TORQUE
PISTON_DIAM_CM = settings.PISTON_DIAM_CM
PISTON_AREA = settings.PISTON_AREA_CM2


def seconds(df):
    """Make a second series to integrate on"""
    df["seconds"] = np.arange(0, len(df.index), 1)
    return df


def lift_load(df):
    """load on the forks in Tons"""
    df["lifted_load"] = 10 * df.lift_pressure_raw * PISTON_AREA / 10000  # in Tons
    return df


def drop_lines_wo_state(df):
    """drop values when category is has no state and enginespeed is 0"""
    df = df.drop(df[df.truck_state == "drop"].index)
    return df


def accel_rates(df):
    """calculate accped and Joystick rate"""
    df["accelp_rate"] = np.gradient(df.accelpedal_pos, df.seconds)
    df["hoist_rate"] = np.gradient(df.hoist_percentage, df.seconds)
    return df


def preprocess():
    """apply all preprocess functions and write to a pickle file"""
    for file in LOADED_PATH.glob("*"):
        try:
            with open(file, "rb") as f:
                df = pickle.load(f)
        except FileNotFoundError:
            print(f"file not found{file}")
            continue

        df = seconds(df)
        df = lift_load(df)
        df = accel_rates(df)
        df = categorize.hydraulic_active(df)
        df = categorize.categorize(df)
        df = drop_lines_wo_state(df)
        df = power_split.power_split(df)
        df = power_split.energy_split(df)
        write_to_pickle(file, df)


def write_to_pickle(file, df):
    try:
        with open(PROCESSED_PATH / file.name, "wb") as f:
            pickle.dump(df, f)
            print(f"preprocessed file {file.name} ")

    except:
        print("failed to make a pickle file")


# def merge_pickles(dir_path: str, output_file: str) -> None:
#     """
#     Merge all .pkl files in a directory into a single .pkl file.

#     Args:
#     dir_path (str): The path to the directory containing the .pkl files.
#     output_file (str): The name of the output .pkl file.

#     Returns:
#     None
#     """
#     # Convert input arguments to Path objects
#     dir_path = Path(dir_path)
#     output_file = Path(output_file)

#     files = list(dir_path.glob("*.pkl"))
#     merged_df = pd.DataFrame()

#     for file in files:
#         try:
#             with open(file, "rb") as pkl_file:
#                 print(f"Opening {file}...")
#                 file_df = pd.read_pickle(pkl_file)
#         except:
#             print(f"Error: Could not load file {file}. Skipping...")
#             continue
#         if not isinstance(file_df, pd.DataFrame):
#             print(f"Error: File {file} does not contain a DataFrame. Skipping...")
#             continue
#         merged_df = pd.concat([merged_df, file_df], axis=0)

#     merged_df = merged_df.sort_index()
#     merged_df.to_pickle(output_file)
#     print(f"Combined {len(files)} files into {output_file}")
#     print(f"Saved merged file to {output_file.resolve()}")


if __name__ == "__main__":
    print("Data loading module not intended as main")
