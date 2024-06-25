#!/usr/bin/env python3

"""
Python Script to Generate the positivity_tally.tsv from DETECTION_RESULTS.tsv for display on Github.
"""

import sys

import pandas as pd


## Function to count unique strings in column 'carton' by a specific condition in column 'positive_for_HPAI' and sum by column 'processing_plant_state'
def count_unique_by_condition(df, condition):
    filtered_df = df[df["positive_for_HPAI"] == condition]
    unique_counts = (
        filtered_df.groupby("processing_plant_state")["carton"].nunique().reset_index()
    )
    unique_counts.columns = ["processing_plant_state", f"Unique_Counts_{condition}"]
    return unique_counts

def count_unique_cartons(df):
    unique_counts = (
        df.groupby("processing_plant_state")["carton"].nunique().reset_index()
    )
    unique_counts.columns = ["processing_plant_state", "Unique_Counts_Total"]
    return unique_counts


def main() -> None:
    """
    script entrypoint
    """

    detection_results = sys.argv[1]
    output_path = sys.argv[2]

    ## Read in the DETECTION_RESULTS.tsv after pulling the latest version from github (https://github.com/dholab/dairy-hpai-monitoring)
    df = pd.read_csv(detection_results, sep="\t")

    ## Convert the date column to datetime format
    df["date_purchased"] = pd.to_datetime(df["date_purchased"])

    ## Make sure needed columns are in string format
    columns_to_convert = ["positive_for_HPAI", "processing_plant_state", "carton"]
    df[columns_to_convert] = df[columns_to_convert].astype(str)

    ## Count for True
    true_counts = count_unique_by_condition(df, "True")

    ## Count for Total
    total_counts = count_unique_cartons(df)

    ## Merge the results into the results dataframe
    results_df = pd.merge(
        total_counts, true_counts, on="processing_plant_state", how="outer"
    ).fillna(0)

    ## Rename the columns to match the required format
    results_df.columns = [
        "Processing Plant State",
        "Total Cartons",
        "Positive Cartons",
    ]

    ## Calculate column "Negative Cartons" as the difference of columns "Total Cartons" and "Positive Cartons"
    results_df["Negative Cartons"] = (
        results_df["Total Cartons"] - results_df["Positive Cartons"]
    )

    ## Find the latest date for each unique string in column "date_purchased"
    latest_dates = (
        df.groupby("processing_plant_state")["date_purchased"].max().reset_index()
    )
    latest_dates.columns = ["Processing Plant State", "Latest Date Sampled"]

    ## Merge the latest dates into the "Results DataFrame"
    results_df = pd.merge(
        results_df, latest_dates, on="Processing Plant State", how="left"
    )

    ## Rearrange columns
    sorted_results_df = results_df[
        [
            "Processing Plant State",
            "Total Cartons",
            "Negative Cartons",
            "Positive Cartons",
            "Latest Date Sampled",
        ]
    ]

    ## Sort the results DataFrame alphabetically by state
    sorted_results_df = results_df.sort_values(by="Processing Plant State")

    # Make all the numbers integers so we don't have to bother with float formatting
    int_cols = ["Total Cartons",
            "Negative Cartons",
            "Positive Cartons",
            ]
    sorted_results_df[int_cols] = sorted_results_df[int_cols].astype(int)

    ## Save sorted_results_df as a tsv file
    sorted_results_df.to_csv(output_path, sep="\t", index=False)


if __name__ == "__main__":
    main()
