from asammdf import MDF
from settings import settings
from pathlib import Path
import pickle
import os

RESAMPLE_FREQ_HZ = settings.resample_freq_Hz

FILTER_LIST = settings.FILTER_LIST

COMMON_NAME = settings.COMMON_NAME

# specify the output directory
loaded_dir = os.path.join(settings.data_dir, "loaded")


def load_input(raw_data_dir, output_dir):
    """This function is used to transform all the MDF4 files to a
    pickle file, filter the channels needed on the hand of the filter
    list, and resamples the data to 1 Hz.
    """

    # create the directory if it doesn't exist
    new_dir(loaded_dir)

    for file in settings.data_raw_dir.glob("*"):
        filtered_mdf = filter_mdf(file)
        resampled_signals = resample_mdf(filtered_mdf)
        df = resampled_signals.to_dataframe(time_as_date=True)
        df.rename(columns=COMMON_NAME, inplace=True)
        f_name = make_unique_filename(file)

        # Write to a pickele file
        try:
            with open(os.path.join(loaded_dir, f_name + ".pkl"), "wb") as f:
                pickle.dump(df, f)  # write the file to the output directory
                print(f"Loaded RAW file {f_name} ")
        except:
            print("failed to make a pickle file")


def new_dir(loaded_dir):
    if not os.path.exists(loaded_dir):
        os.makedirs(loaded_dir)


def make_unique_filename(file):
    """Return a new file name based on the original name. The returned
    name is a combination of the truck name and the date.
    """
    name = Path(file).stem
    components = name.split("_")
    return components[0][:4] + "_" + components[2]


def resample_mdf(filtered_mdf):
    try:
        resampled_signals = filtered_mdf.resample(RESAMPLE_FREQ_HZ)
    except:
        print("MDF resampling failed")
    return resampled_signals


def filter_mdf(file):
    try:
        mdf = MDF(file)
        filtered_mdf = mdf.filter(FILTER_LIST)
    except:
        print("MDF filtering failed")
    return filtered_mdf


if __name__ == "__main__":
    print("Data loading module not intended as main")

