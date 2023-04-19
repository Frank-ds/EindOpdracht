"""this files splits the power per truck state"""
import scipy.integrate as integrate
import numpy as np
import pandas as pd
from settings import settings
from pathlib import Path

REF_TORQUE = settings.REF_TORQUE  # cummin spec sheet  QSB 6.7 tier 4f
PROCESSED_PATH = settings.processed_path
LOADED_PATH = settings.loaded_path


def power_split(df):
    """Splits the power per truck state"""
    df["engine_torque"] = (
        (df.engine_actual_torq - df.NomFrictionPercTorq) * REF_TORQUE / 100
    )
    df["engine_power"] = df.engine_torque * df.engine_speed * 2 * np.pi / 60 / 1000

    df["drive_power"] = df.apply(
        lambda row: row["engine_power"] if row["drive_only"] == True else 0, axis=1
    )
    df["hydr_power"] = df.apply(
        lambda row: row["engine_power"] if row["hydr_only"] == True else 0, axis=1
    )
    df["idle_power"] = df.apply(
        lambda row: row["engine_power"] if row["truck_idle"] == True else 0, axis=1
    )
    df["working_power"] = df.apply(
        lambda row: row["engine_power"] if row["working"] == True else 0, axis=1
    )
    return df


def energy_split(df):
    """Splits the energy per truck state"""
    df["engine_used_energy"] = (
        integrate.cumulative_trapezoid(
            df.engine_power, (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    df["drive_energy"] = (
        integrate.cumulative_trapezoid(
            df.drive_power, (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    df["hydr_energy"] = (
        integrate.cumulative_trapezoid(
            df.hydr_power, (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    df["idle_energy"] = (
        integrate.cumulative_trapezoid(
            df.idle_power, (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    df["working_energy"] = (
        integrate.cumulative_trapezoid(
            df.working_power, (df.index - df.index[0]).total_seconds(), initial=0
        )
        / 3600
    )
    return df
