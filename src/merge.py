"""Merging multiple pickle files into one file"""

import pandas as pd
import pickle
from pathlib import Path
import numpy as np


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


# def power_accumulation(df):
#     max_drive_energy = round(np.max(df.drive_energy), 2)
#     max_hydr_energy = round(np.max(df.hydr_energy), 2)
#     max_working_energy = round(np.max(df.working_energy), 2)
#     max_idle_energy = round(np.max(df.idle_energy), 2)
#     max_engine_energy = round(np.max(df.engine_used_energy), 2)
#     drive_energy_perc = round(max_drive_energy * 100 / max_engine_energy, 2)
#     hydr_energy_perc = round(max_hydr_energy * 100 / max_engine_energy, 2)
#     work_energy_perc = round(max_working_energy * 100 / max_engine_energy, 2)
#     idle_energy_perc = round(max_idle_energy * 100 / max_engine_energy, 2)

#     accum_values = {
#         "drive_energy": max_drive_energy,
#         "hydr_energy": max_hydr_energy,
#         "working_energy": max_working_energy,
#         "idle_energy": max_idle_energy,
#         "engine_energy": max_engine_energy,
#         "drive_%": drive_energy_perc,
#         "hydr_%": hydr_energy_perc,
#         "working_%": work_energy_perc,
#         "idle_%": idle_energy_perc,
#     }

#     # max_df = pd.DataFrame.from_dict(max_values, orient="index", columns=["max_value"])

#     return pd.Series(accum_values)


# def df_accumulation(dir_in_path: str, dir_out_path: str, output_file_name: str):
#     """Makes one df with accumulated values from day df's

#     Args:
#     dir_path (str): The path to the directory containing the .pkl files.
#     dir_path (str): The path to the directory writing .pkl files to.
#     output_file_name (str): The name of the output .pkl file.
#     """
#     dir_in_path = Path(dir_in_path)
#     output_file_path = Path(dir_out_path) / (output_file_name + ".pkl")
#     # dir_in_path = Path(dir_in_path)
#     # output_file = Path(output_file)

#     dfs = {}
#     for file_path in dir_in_path.glob("*.pkl"):
#         file_name = file_path.stem
#         with open(file_path, "rb") as f:
#             df = pd.read_pickle(f)
#             dfs[file_name] = df

#     Accum_values_df = pd.DataFrame()
#     for file_name, df in dfs.items():
#         accum_values = power_accumulation(df)
#         Accum_values_df[file_name] = accum_values

#     Accum_values_df = Accum_values_df.T
#     # output_file_path = dir_out_path / output_file_name / ".pkl"
#     with open(output_file_path, "wb") as f:
#         pd.to_pickle(Accum_values_df, f)


if __name__ == "__main__":
    print("Data loading module not intended as main")
