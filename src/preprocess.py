"""Preprocess data"""
import pandas as pd
import numpy as np
from config import settings

ADDITIONAL_COLUMNS = ["Company Name", "Website", settings.TOTAL_FUNDING_COL] + [
    settings.GROWTH_METRICS[key]["normalize_by"] for key in settings.GROWTH_METRICS
]


def _slope_of_array(series: pd.Series) -> float:
    """
    calculate the slope of the line of the series
    assuming the x axis is the index of the series
    """
    # drop NaN in the series
    series = series.dropna()
    # only calulate the slope if there are at least 2 points
    if len(series) < 3:
        return np.nan
    x = np.arange(len(series))
    y = series
    return np.polyfit(x, y, 1)[0]


def _normalized_growth(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    calculate the normalized growth of a metric
    """

    # get the columns to calculate the growth
    growth_metric_cols = settings.GROWTH_METRICS[metric]["growth"]

    # rows with missing values
    # this does not include rows with all NaN
    # rows_with_missing_values = ~df[growth_metric_cols].isna().all(axis=1)

    # calculate the growth
    normalized_growth = df.copy()[growth_metric_cols].apply(
        lambda x: x / df[settings.GROWTH_METRICS[metric]["normalize_by"]]
    )

    # NOTE: no longer filling NaN with 0 - line of best fit will be able to estimate the growth based on previous points alone
    # # fill NaN with 0 for rows with missing values
    # normalized_growth.loc[
    #     rows_with_missing_values, growth_metric_cols
    # ] = normalized_growth.loc[rows_with_missing_values, growth_metric_cols].fillna(0)

    # calculate the slope of the line of each company
    slopes = (
        normalized_growth[growth_metric_cols]
        .apply(_slope_of_array, axis=1)
        .sort_values(ascending=False)
    )

    normalized_growth[f"{metric}_slope"] = slopes

    return normalized_growth


def _final_kpi(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    """
    calculate the final KPI - weighted average of the slopes
    """
    # final KPI is a weighted average of the slopes
    # NOTE: if the metric_slope if NaN, then it is ignored by pandas mean function
    df["growth_kpi"] = df[[f"{metric}_slope" for metric in metrics]].mean(axis=1)

    # normalise the final KPI from 0 to 1
    df["growth_kpi"] = (df["growth_kpi"] - df["growth_kpi"].min()) / (
        df["growth_kpi"].max() - df["growth_kpi"].min()
    )

    # sort by final KPI
    df = df.sort_values(by="growth_kpi", ascending=False)

    return df


def main(df: pd.DataFrame, top_n: int, metrics=[]) -> pd.DataFrame:
    """
    get preprocessed data - with growth metrics and final KPI
    """

    # calculate slopes for each metric
    metric_growth_rates = []

    if metrics == []:
        metrics = settings.GROWTH_METRICS

    for metric in metrics:
        # calculate the normalized growth rates
        metric_growth_rates.append(_normalized_growth(df, metric))

    # merge all growth rates into one df - based on Specter - ID
    _processed_data = pd.concat(metric_growth_rates, axis=1)

    # add additional columns
    processed_data = pd.concat([df[ADDITIONAL_COLUMNS], _processed_data], axis=1)

    # final KPI is a weighted average of the slopes
    processed_data = _final_kpi(processed_data, metrics)

    # get top n
    processed_data = processed_data.head(top_n)

    return processed_data
