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

    ## Create a results dataframe
    results_df = pd.DataFrame(columns=["A", "B", "C", "D"])

    ## Count for True
    true_counts = count_unique_by_condition(df, "True")

    ## Count for False
    false_counts = count_unique_by_condition(df, "False")

    ## Merge the results into the results dataframe
    results_df = pd.merge(
        false_counts, true_counts, on="processing_plant_state", how="outer"
    ).fillna(0)

    ## Rename the columns to match the required format
    results_df.columns = [
        "Processing Plant State",
        "Negative Cartons",
        "Positive Cartons",
    ]

    ## Calculate column "Total Cartons" as the sum of columns "Negative Cartons" and "Positive Cartons"
    results_df["Total Cartons"] = (
        results_df["Negative Cartons"] + results_df["Positive Cartons"]
    )

    ## Find the latest date for each unique string in column '2'
    latest_dates = (
        df.groupby("processing_plant_state")["date_purchased"].max().reset_index()
    )
    latest_dates.columns = ["Processing Plant State", "As of"]

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
            "As of",
        ]
    ]

    ## Sort the results DataFrame alphabetically by state
    sorted_results_df = results_df.sort_values(by="Processing Plant State")

    ## Save sorted_results_df as a tsv file
    sorted_results_df.to_csv(output_path, sep="\t", index=False, float_format="%.01g")


if __name__ == "__main__":
    main()
