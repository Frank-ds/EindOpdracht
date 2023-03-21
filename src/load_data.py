from asammdf import MDF
from settings import settings
import pathlib as Path
import pickle
import os

# signal selection
FILTER_LIST = [
    "TCU_CCVS_Wheelbasedvehiclespeed",
    "HS_Lift_Height",
    "ECM_EEC1_Engine_Speed",
    "ECM_EEC2_AccelPedalPos1",
    "ECM_EEC1_Engine_Actual_Eng_Torqu",
    "ECM_EEC2_EngPercLoadAtCurrSpd",
    "ECM_EEC3_NomFrictionPercTorq",
    "ECM_LFE1_FuelRate",
    "JOY_BJM1_Hoist_Percentage",
    "GPS_latitude",
    "GPS_longitude",
    "GPS_speed",
    "GPS_altitude",
    "PS_Pressure_Sensor_Lift",
    "PS_Sensor_Brake",
    "JOY_BJM1_Hoist_Lift_Status",
    "JOY_BJM1_Hoist_Lower_Status",
    "JOY_BJM1_Tilt_Forward_Status",
    "JOY_BJM1_Tilt_Backward_Status",
    "JOY_EJM1_PileSlope_Back_Status",
    "JOY_EJM1_PileSlope_Fwd_Status",
    "JOY_BJM1_Spreader_Extend",
    "JOY_BJM1_Spreader_Retract",
    "JOY_BJM1_Spreader_SideShiftLeft",
    "JOY_BJM1_Spreader_SideShiftRight",
    "JOY_BJM1_Spreader_Twist_Unlock",
    "JOY_BJM1_Spreader_Twistlock_Lock",
]
# print(filter_list)

# Commonname list
CNAME_DICT = {
    "HS_Lift_Height": "Lift_Height",
    "TCU_CCVS_Wheelbasedvehiclespeed": "Vehicle_speed",
    "ECM_EEC1_Engine_Speed": "Engine_Speed",
    "ECM_EEC2_AccelPedalPos1": "AccelPedalPos",
    "JOY_BJM1_Hoist_Percentage": "Hoist_Percentage",
    "ECM_EEC1_Engine_Actual_Eng_Torqu": "Engine_Actual_Torq",
    "ECM_EEC2_EngPercLoadAtCurrSpd": "EngPercLoadAtCurrSp",
    "ECM_EEC3_NomFrictionPercTorq": "NomFrictionPercTorq",
    "ECM_LFE1_FuelRate": "FuelRate",
    "PS_Pressure_Sensor_Lift": "Lift_pressure_raw",
    "PS_Sensor_Brake": "Brake_pressure_raw",
    "GPS_latitude": "lat",
    "GPS_longitude": "lon",
    "JOY_BJM1_Hoist_Lift_Status": "Lift_Status",
    "JOY_BJM1_Hoist_Lower_Status": "Lower_Status",
    "JOY_BJM1_Tilt_Forward_Status": "Tilt_Fwd",
    "JOY_BJM1_Tilt_Backward_Status": "Tilt_Bwd",
    "JOY_EJM1_PileSlope_Back_Status": "PPS_Bwd",
    "JOY_EJM1_PileSlope_Fwd_Status": "PPS_Fwd",
    "JOY_BJM1_Spreader_Extend": "Spr_Extend",
    "JOY_BJM1_Spreader_Retract": "Spr_Retract",
    "JOY_BJM1_Spreader_SideShiftLeft": "SS_Left",
    "JOY_BJM1_Spreader_SideShiftRight": "SS_Right",
    "JOY_BJM1_Spreader_Twist_Unlock": "TWL_Unlock",
    "JOY_BJM1_Spreader_Twistlock_Lock": "TWL_Lock",
}

# specify the output directory
proces_dir = os.path.join(settings.data_dir, "converted")

# create the directory if it doesn't exist
if not os.path.exists(proces_dir):
    os.makedirs(proces_dir)

for file in settings.data_raw_dir.glob("*"):
    mdf = MDF(file)
    filtered_mdf = mdf.filter(FILTER_LIST)  # Filter signals in mdf file
    resampled_signals = filtered_mdf.resample(1)  # resample to 1Hz
    df = resampled_signals.to_dataframe()  # mdf to pandas dataframe
    df.rename(columns=CNAME_DICT, inplace=True)  # rename signals

    # make a unique filename
    file_name = os.path.basename(file)
    f_name = os.path.splitext(file_name)[0]
    f_name = os.path.splitext(file_name)[0][:4] + os.path.splitext(file_name)[0][14:21]

    # Write to a pickele file
    with open(os.path.join(proces_dir, f_name + ".pkl"), "wb") as f:
        pickle.dump(df, f)  # write the file to the output directory

# loop true all the files
mdf = MDF(settings.file_path)
if __name__ == "__main__":
    # for file in settings.data_raw_dir.glob("*"):
    #     f_name = file.name.split("_")[2]
    print("done")
