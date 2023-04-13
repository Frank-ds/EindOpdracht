"""this files splits the power per truck state"""
import scipy.integrate as integrate
import numpy as np
import pandas as pd


def power_split(df):
    """Splits the power per truck state"""
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
    df["drive_energy"] = (
        integrate.cumulative_trapezoid(df.drive_power, df.seconds, initial=0) / 3600
    )
    df["hydr_energy"] = (
        integrate.cumulative_trapezoid(df.hydr_power, df.seconds, initial=0) / 3600
    )
    df["idle_energy"] = (
        integrate.cumulative_trapezoid(df.idle_power, df.seconds, initial=0) / 3600
    )
    df["working_energy"] = (
        integrate.cumulative_trapezoid(df.working_power, df.seconds, initial=0) / 3600
    )
    return df
