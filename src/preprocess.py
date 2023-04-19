import pydantic
from asammdf import MDF
from pathlib import Path
import numpy as np


class _Settings(pydantic.BaseSettings):
    base_dir: Path = Path(__file__).parents[1]
    data_dir: Path = base_dir / "data"
    data_raw_dir: Path = data_dir / "RAW"
    loaded_path: Path = data_dir / "loaded"
    processed_path: Path = data_dir / "Processed"
    resample_freq_Hz: float = 1.0
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
    COMMON_NAME = {
        "HS_Lift_Height": "lift_height",
        "TCU_CCVS_Wheelbasedvehiclespeed": "vehicle_speed",
        "ECM_EEC1_Engine_Speed": "engine_speed",
        "ECM_EEC2_AccelPedalPos1": "accelpedal_pos",
        "JOY_BJM1_Hoist_Percentage": "hoist_percentage",
        "ECM_EEC1_Engine_Actual_Eng_Torqu": "engine_actual_torq",
        "ECM_EEC2_EngPercLoadAtCurrSpd": "EngPercLoadAtCurrSp",
        "ECM_EEC3_NomFrictionPercTorq": "NomFrictionPercTorq",
        "ECM_LFE1_FuelRate": "fuel_rate",
        "PS_Pressure_Sensor_Lift": "lift_pressure_raw",
        "PS_Sensor_Brake": "brake_pressure_raw",
        "GPS_latitude": "lat",
        "GPS_longitude": "lon",
        "JOY_BJM1_Hoist_Lift_Status": "lift_status",
        "JOY_BJM1_Hoist_Lower_Status": "lower_status",
        "JOY_BJM1_Tilt_Forward_Status": "tilt_fwd",
        "JOY_BJM1_Tilt_Backward_Status": "tilt_bwd",
        "JOY_EJM1_PileSlope_Back_Status": "PPS_bwd",
        "JOY_EJM1_PileSlope_Fwd_Status": "PPS_fwd",
        "JOY_BJM1_Spreader_Extend": "spr_extend",
        "JOY_BJM1_Spreader_Retract": "spr_retract",
        "JOY_BJM1_Spreader_SideShiftLeft": "SS_left",
        "JOY_BJM1_Spreader_SideShiftRight": "SS_right",
        "JOY_BJM1_Spreader_Twist_Unlock": "TWL_unlock",
        "JOY_BJM1_Spreader_Twistlock_Lock": "TWL_lock",
    }
    # meta data
    REF_TORQUE = 1030  # cummin spec sheet  QSB 6.7 tier 4f
    PISTON_DIAM_CM = 12.5
    PISTON_AREA_CM2 = ((PISTON_DIAM_CM**2) * np.pi) / 8  # dev 8 for 2 cilinders


settings = _Settings()
