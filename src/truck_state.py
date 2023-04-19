import pandas as pd


def Func_Active(f1, f2):
    if f1 == True or f2 == True:
        return 1
    else:
        return 0


# df['Hoist_Active']= df.apply(lambda row:['Lift_Status'] : 1 if 500 < x < 920 else 0)
df["Hoist_Active"] = df.apply(
    lambda row: Func_Active(row["Lift_Status"], row["Lower_Status"]), axis=1
)
df["Tilt_Active"] = df.apply(
    lambda row: Func_Active(row["Tilt_Fwd"], row["Tilt_Bwd"]), axis=1
)
df["PPS_Active"] = df.apply(
    lambda row: Func_Active(row["PPS_Fwd"], row["PPS_Bwd"]), axis=1
)
df["SS_Active"] = df.apply(
    lambda row: Func_Active(row["SS_Left"], row["SS_Right"]), axis=1
)
df["Spr_Ext_Ret"] = df.apply(
    lambda row: Func_Active(row["Spr_Extend"], row["Spr_Retract"]), axis=1
)
df["TWL_Active"] = df.apply(
    lambda row: Func_Active(row["TWL_Lock"], row["TWL_Unlock"]), axis=1
)


# make a signal to see if the truck is hydraulic is active
def hydraulic_active(lift, tilt, pps, ss, spr, twl):
    if lift or tilt or pps or ss or spr or twl:
        return 1
    else:
        return 0


df["Hydr_Active"] = df.apply(
    lambda row: hydraulic_active(
        row["Hoist_Active"],
        row["Tilt_Active"],
        row["PPS_Active"],
        row["SS_Active"],
        row["Spr_Ext_Ret"],
        row["TWL_Active"],
    ),
    axis=1,
)


# Define driving state
def drive_only(Speed, Hydr):
    """Gives True when driving is active and Hydraulic is False"""
    if Speed >= 0.5 and not Hydr:
        return 1
    else:
        return 0


df["Drive_only"] = df.apply(
    lambda row: drive_only(row["Vehicle_speed"], row["Hydr_Active"]), axis=1
)


# Hydraulic only
def hydr_only(Hydr, Drive):
    """Gives True when driving is false and Hydraulic is active"""
    if not Drive and Hydr:
        return 1
    else:
        return 0


df["Hydr_only"] = df.apply(
    lambda row: hydr_only(row["Hydr_Active"], row["Drive_only"]), axis=1
)

# make a signal to see if the engine is idling
df["Engine_Idle"] = df["Engine_Speed"].apply(lambda x: 1 if 500 < x < 920 else 0)


# Function to determine idle state, Gives true when idle is true and drv is false
def truck_idle(idle_active, drv_active, hydr_active):
    """Gives true when idle is true and drv is false"""
    if idle_active and not drv_active and not hydr_active:
        return 1
    else:
        return 0


# apply the function with lambda
df["Truck_Idle"] = df.apply(
    lambda row: truck_idle(row["Engine_Idle"], row["Drive_only"], row["Hydr_only"]),
    axis=1,
)


# truck state
def truck_state(idle, drive, hydr):
    if drive and hydr:
        return "Working"
    elif hydr:
        return "Hydraulic"
    elif drive:
        return "Driving"
    elif idle:
        return "Idle"
    else:
        return "None"


df["Truck_State"] = df.apply(
    lambda row: truck_state(row["Truck_Idle"], row["Drive_only"], row["Hydr_only"]),
    axis=1,
)
