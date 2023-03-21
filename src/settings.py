import pydantic
from asammdf import MDF
from pathlib import Path


class _Settings(pydantic.BaseSettings):
    base_dir: Path = Path(__file__).parents[1]
    data_dir: Path = base_dir / "data"
    data_raw_dir: Path = data_dir / "RAW"
    file_path: Path = data_raw_dir / r"E214E01752T_R4_230129_whole_Day.mf4"


settings = _Settings()
