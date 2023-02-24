"""Preprocess data"""
import pandas as pd
import numpy as np
from config import settings
from sklearn.preprocessing import quantile_transform

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

    # calculate the growth
    normalized_growth = df.copy()[growth_metric_cols].apply(
        lambda x: x / df[settings.GROWTH_METRICS[metric]["normalize_by"]]
    )

    # calculate the slope of the line of each company
    slopes = (
        normalized_growth[growth_metric_cols]
        .apply(_slope_of_array, axis=1)
        .sort_values(ascending=False)
    )

    normalized_growth[f"{metric}_slope"] = slopes

    # transform the slope using quantile_transform
    normalized_growth[f"{metric}_slope"] = quantile_transform(
        normalized_growth[[f"{metric}_slope"]], output_distribution="normal"
    )

    return normalized_growth


def _final_kpi(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    """
    calculate the final KPI - weighted average of the slopes
    """
    # final KPI is a weighted average of the slopes
    # NOTE: if the metric_slope if NaN, then it is ignored by pandas mean function
    df["Ranking"] = df[[f"{metric}_slope" for metric in metrics]].mean(axis=1)

    # normalise the final KPI from 0 to 1
    df["Ranking"] = (df["Ranking"] - df["Ranking"].min()) / (
        df["Ranking"].max() - df["Ranking"].min()
    )

    # sort by final KPI
    df = df.sort_values(by="Ranking", ascending=False)

    return df


def preprocessor(df: pd.DataFrame, metrics=None) -> pd.DataFrame:
    """
    get preprocessed data - with growth metrics and final KPI
    """

    # calculate slopes for each metric
    metric_growth_rates = []

    # if metrics is not specified, use all metrics
    if metrics is None:
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

    return processed_data
