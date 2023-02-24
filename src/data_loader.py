import pandas as pd
from config import settings
from functools import lru_cache


@lru_cache(maxsize=256)
def load_data(data_file: str) -> pd.DataFrame:
    """
    Load data from /data directory
    """
    date_cols = ["Last Updated"]
    df = pd.read_csv(
        settings.DATA_PATH.joinpath(data_file),
        index_col="ID",
        parse_dates=date_cols,
    )

    # if NaN total funding, set to 0
    df[settings.TOTAL_FUNDING_COL] = df[settings.TOTAL_FUNDING_COL].fillna(0)

    return df
