#!/usr/bin/env python3

"""
The library `normalize` contains a set of functions that can be called to
normalize a proposed milk HPAI detection update prior to merging with the main branch.
Symbols in its namespace can be called in a Python module like so:

```python3
from .normalize import remove_duplicate_rows, validate_asset_files
```
"""

import os
import sys

import polars as pl


async def validate_asset_files(input_table: pl.LazyFrame, assets_path: str) -> None:
    """
    Validate the presence of primer and probe asset files in a specified directory.

    Args:
        input_table (pl.LazyFrame): The input LazyFrame containing columns for primer and probe asset filenames.
        assets_path (str): The path to the directory where the asset files should be located.

    This function performs the following validations:
        1. Checks if the provided assets_path directory exists.
        2. Verifies that the input_table contains the required columns 'primer_asset_file' and 'probe_asset_file'.
        3. Retrieves the list of expected primer and probe asset files from the input_table,
           excluding any rows with 'REDACTED' values.
        4. Compares the expected asset files with the actual files present in the assets_path directory.
        5. If any expected asset files are missing, it prints a message listing the missing files and exits with a non-zero status code.
        6. If all expected asset files are present, it prints a success message and returns.

    If no primer or probe asset files are found in the input_table, the function will return without performing any validations.

    Note: This function does not return any value, as it either exits with a non-zero status code upon detecting missing files
    or completes silently when all files are present.
    """
    # check that the assets path exists
    assert os.path.isdir(
        assets_path
    ), f"The provided assets folder path, {assets_path} is not found where expected."

    # make sure the file colums exist
    assert (
        "primer_asset_file" in input_table.columns
    ), "Column 'primer_asset_file' is missing in input table."
    assert (
        "probe_asset_file" in input_table.columns
    ), "Column 'probe_asset_file' is missing in input table."

    # list all files in the assets directory
    asset_files = os.listdir(assets_path)

    # pull out expected primer files from table
    expected_primer_files = (
        input_table.select("primer_asset_file")
        .filter(pl.col("primer_asset_file") != "REDACTED")
        .collect()
        .to_series()
        .to_list()
    )
    if len(expected_primer_files) == 0:
        return

    # pull out expected probe files from table
    expected_probe_files = (
        input_table.select("probe_asset_file")
        .filter(pl.col("probe_asset_file") != "REDACTED")
        .collect()
        .to_series()
        .to_list()
    )
    if len(expected_primer_files) == 0:
        return

    # check that all of each kind of file are in the assets folder
    missing_primer_files = [
        file for file in expected_primer_files if file not in asset_files
    ]
    missing_probe_files = [
        file for file in expected_probe_files if file not in asset_files
    ]
    all_missing_files = missing_primer_files + missing_probe_files

    # if there are no missing files, early return
    if len(all_missing_files) == 0:
        print("All primer files present in `assets/`.")
        return

    # and if there were missing files, report them an exit with status 1
    print(
        f"The following files in the metadata were missing in assets. Please double check your submission:\n{all_missing_files}"
    )
    sys.exit(1)


async def remove_duplicate_rows(input_table: pl.LazyFrame) -> pl.LazyFrame:
    """
    Remove duplicate rows from a Polars LazyFrame.

    Args:
        input_table (pl.LazyFrame): The input LazyFrame containing potential duplicate rows.

    Returns:
        pl.LazyFrame: A new LazyFrame with all duplicate rows removed, preserving the original order.

    This function takes a Polars LazyFrame as input and returns a new LazyFrame with all
    duplicate rows removed. The resulting LazyFrame preserves the original order of the
    non-duplicate rows from the input LazyFrame.
    """
    return input_table.unique()
