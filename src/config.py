"""pydantic config class for the project"""

import pathlib
from pydantic import BaseSettings


class Settings(BaseSettings):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    FILE_NAME = "taxonomy_result.csv"

    # metric mapping for growth indicators
    GROWTH_METRICS = {
        "employees": {
            "normalize_by": "Employee Count",
            "growth": [
                "Employees - Monthly Growth",
                "Employees - 2 Months Growth",
                "Employees - 3 Months Growth",
                "Employees - 4 Months Growth",
                "Employees - 5 Months Growth",
                "Employees - 6 Months Growth",
            ],
        },
        "web_visits": {
            "normalize_by": "Web Visits",
            "growth": [
                "Web Visits - Monthly Growth",
                "Web Visits - 2 Months Growth",
                "Web Visits - 3 Months Growth",
                "Web Visits - 4 Months Growth",
                "Web Visits - 5 Months Growth",
                "Web Visits - 6 Months Growth",
            ],
        },
        "web_popularity_rank": {
            "normalize_by": "Website Popularity Rank",
            "growth": [
                "Website Popularity Rank - Monthly Growth",
                "Website Popularity Rank - 2 Months Growth",
                "Website Popularity Rank - 3 Months Growth",
                "Website Popularity Rank - 4 Months Growth",
                "Website Popularity Rank - 5 Months Growth",
                "Website Popularity Rank - 6 Months Growth",
            ],
        },
        "linkedin_followers": {
            "normalize_by": "LinkedIn - Followers",
            "growth": [
                "LinkedIn - Monthly Followers Growth",
                "LinkedIn - 2 Months Followers Growth",
                "LinkedIn - 3 Months Followers Growth",
                "LinkedIn - 4 Months Followers Growth",
                "LinkedIn - 5 Months Followers Growth",
                "LinkedIn - 6 Months Followers Growth",
            ],
        },
        "twitter_followers": {
            "normalize_by": "Twitter - Followers",
            "growth": [
                "Twitter - Monthly Followers Growth",
                "Twitter - 2 Months Followers Growth",
                "Twitter - 3 Months Followers Growth",
                "Twitter - 4 Months Followers Growth",
                "Twitter - 5 Months Followers Growth",
                "Twitter - 6 Months Followers Growth",
            ],
        },
        "instagram_followers": {
            "normalize_by": "Instagram - Followers",
            "growth": [
                "Instagram - Monthly Followers Growth",
                "Instagram - 2 Months Followers Growth",
                "Instagram - 3 Months Followers Growth",
                "Instagram - 4 Months Followers Growth",
                "Instagram - 5 Months Followers Growth",
                "Instagram - 6 Months Followers Growth",
            ],
        },
        "app_downloads": {
            "normalize_by": "Total App Downloads",
            "growth": [
                "Total App Downloads - Monthly Growth",
                "Total App Downloads - 2 Months Growth",
                "Total App Downloads - 3 Months Growth",
                "Total App Downloads - 4 Months Growth",
                "Total App Downloads - 5 Months Growth",
                "Total App Downloads - 6 Months Growth",
            ],
        },
        "itunes_reviews": {
            "normalize_by": "iTunes - Reviews",
            "growth": [
                "iTunes - Monthly Reviews Growth",
                "iTunes - 2 Months Reviews Growth",
                "iTunes - 3 Months Reviews Growth",
                "iTunes - 4 Months Reviews Growth",
                "iTunes - 5 Months Reviews Growth",
                "iTunes - 6 Months Reviews Growth",
            ],
        },
        "google_play_reviews": {
            "normalize_by": "Google Play - Reviews",
            "growth": [
                "Google Play - Monthly Reviews Growth",
                "Google Play - 2 Months Reviews Growth",
                "Google Play - 3 Months Reviews Growth",
                "Google Play - 4 Months Reviews Growth",
                "Google Play - 5 Months Reviews Growth",
                "Google Play - 6 Months Reviews Growth",
            ],
        },
    }

    # funding column name
    TOTAL_FUNDING_COL = "Total Funding Amount (in USD)"

    # default to $ 20m
    DEFAULT_FUNDING_FILTER = 20000000

    # TODO: this should be a secret
    VALID_USERNAME_PASSWORD_PAIRS = {"tommy": "specter"}

    # set VERSION to default value
    VERSION = "0.0.0"

    # version from version.env file
    class Config:
        env_file = "version.env"


settings = Settings()
