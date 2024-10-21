#!/usr/bin/env python3

"""
This script processes detection results for HPAI (Highly Pathogenic Avian Influenza) and generates a summary report.

Usage:
    python positivity_tally.py <input_file> <output_file>

Arguments:
    <input_file>: Path to the input TSV file containing detection results.
    <output_file>: Path where the output TSV file will be saved.

Input file format:
    The input file should be a tab-separated values (TSV) file with the following columns:
    - date_purchased: Date of purchase (will be converted to a date object)
    - processing_plant_state: State where the processing plant is located
    - carton: Carton identifier
    - positive_for_HPAI: Boolean indicating whether the sample tested positive for HPAI

Output:
    The script will generate a TSV file with the following columns:
    - Processing Plant State: State where the processing plant is located
    - Total Cartons: Total number of cartons tested
    - Positive Cartons: Number of cartons that tested positive for HPAI
    - Negative Cartons: Number of cartons that tested negative for HPAI
    - Latest Date Sampled: Most recent date when samples were taken for each state

Required libraries:
    - polars

Example:
    python positivity_tally.py input_data.tsv output_summary.tsv
"""

import sys

import polars as pl


def parse_input_results(detection_results: str) -> pl.LazyFrame:
    """
    Parse input results from a TSV file and apply transformations.

    This function reads a TSV file containing detection results,
    converts the date_purchased column to a date column, and
    renames the processing_plant_state column.

    Args:
        detection_results (str): Path to the input TSV file.

    Returns:
        pl.LazyFrame: A LazyFrame with the parsed and transformed data.
    """
    return (
        pl.scan_csv(detection_results, separator="\t", infer_schema_length=1000)
        .with_columns(
            pl.col("date_purchased").str.to_date().alias("date_purchased"),
        )
        .rename({"processing_plant_state": "Processing Plant State"})
    )


def tally_all_cartons(detections: pl.LazyFrame) -> pl.LazyFrame:
    """
    Tally all cartons in the detection results.

    This function counts the total number of cartons for each processing plant state.

    Args:
        detections (pl.LazyFrame): A LazyFrame containing the detection results.

    Returns:
        pl.LazyFrame: A LazyFrame with the total carton count for each state.
    """
    return (
        detections.select("Processing Plant State", "carton")
        .group_by("Processing Plant State")
        .len()
        .rename({"len": "Total Cartons"})
    )


def count_positive_detections(detections: pl.LazyFrame) -> pl.LazyFrame:
    """
    Count the number of positive HPAI detections for each processing plant state.

    This function filters the detections for positive HPAI results,
    counts the number of positive cartons for each state, and renames
    the resulting column.

    Args:
        detections (pl.LazyFrame): A LazyFrame containing the detection results.

    Returns:
        pl.LazyFrame: A LazyFrame with the positive carton count for each state.
    """
    return (
        detections.filter(pl.col("positive_for_HPAI").eq(True))  # noqa: FBT003
        .select("Processing Plant State", "carton")
        .group_by("Processing Plant State")
        .len()  # this should be changed to `.n_unique()` for unique cartons only
        .rename({"len": "Positive Cartons"})
    )


def count_negative_detections(detections: pl.LazyFrame) -> pl.LazyFrame:
    """
    Count the number of negative HPAI detections for each processing plant state.

    This function filters the detections for negative HPAI results,
    counts the number of negative cartons for each state, and renames
    the resulting column.

    Args:
        detections (pl.LazyFrame): A LazyFrame containing the detection results.

    Returns:
        pl.LazyFrame: A LazyFrame with the negative carton count for each state.
    """
    return (
        detections.filter(pl.col("positive_for_HPAI").eq(False))  # noqa: FBT003
        .select("Processing Plant State", "carton")
        .group_by("Processing Plant State")
        .len()  # this should be changed to `.n_unique()` for unique cartons only
        .rename({"len": "Negative Cartons"})
    )


def find_latest_sampling_dates(detections: pl.LazyFrame) -> pl.LazyFrame:
    """
    Find the latest sampling dates for each processing plant state.

    This function groups the detections by processing plant state,
    finds the maximum (latest) date for each state, and renames
    the result column.

    Args:
        detections (pl.LazyFrame): A LazyFrame containing the detection results.

    Returns:
        pl.LazyFrame: A LazyFrame with the latest sampling date for each state.
    """
    return (
        detections.select("Processing Plant State", "date_purchased")
        .group_by("Processing Plant State")
        .max()
        .rename({"date_purchased": "Latest Date Sampled"})
    )


def generate_final_results(
    total_tested: pl.LazyFrame,
    negative_counts: pl.LazyFrame,
    positive_counts: pl.LazyFrame,
    latest_dates: pl.LazyFrame,
) -> pl.LazyFrame:
    """
    Generate final results by joining different LazyFrames.

    This function takes four LazyFrames containing different aspects of the
    detection results and joins them together to create a final result set.
    It also applies some additional transformations to the data.

    Args:
        total_tested (pl.LazyFrame): LazyFrame with total carton counts.
        negative_counts (pl.LazyFrame): LazyFrame with negative detection counts.
        positive_counts (pl.LazyFrame): LazyFrame with positive detection counts.
        latest_dates (pl.LazyFrame): LazyFrame with latest sampling dates.

    Returns:
        pl.LazyFrame: A LazyFrame with the final combined results.
    """
    return (
        total_tested.join(
            positive_counts,
            on="Processing Plant State",
            how="left",
            validate="1:1",
        )
        .join(
            negative_counts,
            on="Processing Plant State",
            how="left",
            validate="1:1",
        )
        .join(
            latest_dates,
            on="Processing Plant State",
            how="left",
            validate="1:1",
        )
        .fill_null(0)
        .sort("Processing Plant State")
    )


def main() -> None:
    """
    Script entrypoint
    """
    # pull input and output information from the command line
    detection_results = sys.argv[1]
    output_path = sys.argv[2]

    # parse the input detection results
    detections = parse_input_results(detection_results)

    # determine how many cartons were tested
    total_tested = tally_all_cartons(detections)

    # count positive detections
    positive_counts = count_positive_detections(detections)

    # count negative detections
    negative_counts = count_negative_detections(detections)

    # count the latest dates in which testing occurred for each state
    latest_dates = find_latest_sampling_dates(detections)

    # use a series of left joins to generate the final results that will be written
    # out to a TSV
    final_results = generate_final_results(
        total_tested,
        positive_counts,
        negative_counts,
        latest_dates,
    )

    # do the writing
    final_results.collect().write_csv(output_path, separator="\t")


if __name__ == "__main__":
    main()
