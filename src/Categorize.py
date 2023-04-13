"""Categorize truck functions into drive hydraulic usage working idle and non catogorized"""
import pandas as pd


# State to see when Hydraulic is active
def Func_Active(f1, f2):
    """Gives True when one of the two booleans are TRUE"""
    if f1 == True or f2 == True:
        return 1
    else:
        return 0


def hydraulic_combi(lift, tilt, pps, ss, spr):
    """make a signal to see if the truck is hydraulic is active"""
    if lift or tilt or pps or ss or spr:
        return 1
    else:
        return 0


def hydraulic_active(df):
    df["hoist_active"] = df.apply(
        lambda row: Func_Active(row["lift_status"], row["lower_status"]), axis=1
    )
    df["tilt_active"] = df.apply(
        lambda row: Func_Active(row["tilt_fwd"], row["tilt_bwd"]), axis=1
    )
    df["PPS_active"] = df.apply(
        lambda row: Func_Active(row["PPS_fwd"], row["PPS_bwd"]), axis=1
    )
    df["SS_active"] = df.apply(
        lambda row: Func_Active(row["SS_left"], row["SS_right"]), axis=1
    )
    df["spr_ext_ret"] = df.apply(
        lambda row: Func_Active(row["spr_extend"], row["spr_retract"]), axis=1
    )
    df["TWL_active"] = df.apply(
        lambda row: Func_Active(row["TWL_lock"], row["TWL_unlock"]), axis=1
    )
    df["hydr_active"] = df.apply(
        lambda row: hydraulic_combi(
            row["hoist_active"],
            row["tilt_active"],
            row["PPS_active"],
            row["SS_active"],
            row["spr_ext_ret"],
        ),
        axis=1,
    )
    return df


# Function to define driving only state
def drive_only(Speed, Hydr):
    """Gives True when driving is active and Hydraulic is False"""
    if Speed >= 0.1 and not Hydr:
        return 1
    else:
        return 0


#  Function to define Hydraulic only
def hydr_only(Hydr, Drive):
    """Gives True when driving is false and Hydraulic is active"""
    if not Drive and Hydr:
        return 1
    else:
        return 0


# Function to define working state
def working(Hydr, speed):
    """Gives True when driving is True and Hydraulic is active"""
    if speed >= 0.1 and Hydr:
        return 1
    else:
        return 0


# Function to determine idle state, Gives true when idle is true and drv is false
def truck_idle(idle_active, drv_active, hydr_active):
    """Gives true when engine is idling vehicle speed is below 0.5 km/h"""
    if idle_active and not drv_active and not hydr_active:
        return 1
    else:
        return 0


def no_state(drive_only, hydr_only, working, truck_idle, eng_speed):
    """returns True when nostate and engine speed is above 0 RPM"""
    if (
        not drive_only
        and not hydr_only
        and not working
        and not truck_idle
        and eng_speed > 0
    ):
        return 1
    else:
        return 0


# truck state
def truck_state(idle, veh_speed, hydr, work, no_state):
    """Defines operating state of the truck"""
    if work:
        return "Working"
    elif hydr:
        return "Hydraulic"
    elif veh_speed:
        return "Driving"
    elif idle:
        return "Idle"
    elif no_state:
        return "NoState"
    else:
        return "drop"


def categorize(df):
    """Categorized the state of the truck, in idle,hydraulic,driving or working"""
    df["drive_only"] = df.apply(
        lambda row: drive_only(row["vehicle_speed"], row["hydr_active"]), axis=1
    )

    df["hydr_only"] = df.apply(
        lambda row: hydr_only(row["hydr_active"], row["drive_only"]), axis=1
    )

    df["working"] = df.apply(
        lambda row: working(row["hydr_active"], row["vehicle_speed"]), axis=1
    )

    df["engine_idle"] = df["engine_speed"].apply(lambda x: 1 if 500 < x < 920 else 0)

    df["truck_idle"] = df.apply(
        lambda row: truck_idle(row["engine_idle"], row["drive_only"], row["hydr_only"]),
        axis=1,
    )

    df["no_state"] = df.apply(
        lambda row: no_state(
            row["drive_only"],
            row["hydr_only"],
            row["working"],
            row["truck_idle"],
            row["engine_speed"],
        ),
        axis=1,
    )

    df["truck_state"] = df.apply(
        lambda row: truck_state(
            row["truck_idle"],
            row["drive_only"],
            row["hydr_only"],
            row["working"],
            row["no_state"],
        ),
        axis=1,
    )

    return df
