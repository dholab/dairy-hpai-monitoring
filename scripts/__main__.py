#!/usr/bin/env python3

"""
Coordinate data flow through our library of normalization functions to ensure
the integrity of the data at https://github.com/dholab/dairy-hpai-monitoring
"""

import argparse
import asyncio
import os
from pathlib import Path

import polars as pl
from normalize import remove_duplicate_rows, validate_asset_files



GIT_MILK_BANNER = r"""
                ___                              ___   ___                        
          .-.  (   )                       .-.  (   ) (   )           .---.       
  .--.   ( __)  | |_        ___ .-. .-.   ( __)  | |   | |   ___     /  _   \    
 /    \  (''") (   __)     (   )   '   \  (''")  | |   | |  (   )   | |   `. .    
;  ,-. '  | |   | |         |  .-.  .-. ;  | |   | |   | |  ' /    (___)   | |    
| |  | |  | |   | | ___     | |  | |  | |  | |   | |   | |,' /          .-'_/     
| |  | |  | |   | |(   )    | |  | |  | |  | |   | |   | .  '.          | |       
| |  | |  | |   | | | |     | |  | |  | |  | |   | |   | | `. \         |_|       
| '  | |  | |   | ' | |     | |  | |  | |  | |   | |   | |   \ \                  
'  `-' |  | |   ' `-' ;     | |  | |  | |  | |   | |   | |    \ .       .-.       
 `.__. | (___)   `.__.     (___)(___)(___)(___) (___) (___ ) (___)     (   )      
 ( `-' ;                                                                `-'       
  `.__.                                                                           
"""


def parse_command_line_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_table",
        "-i",
        type=Path,
        required=True,
        help="Proposed table to be normalized before submission and release.",
    )
    parser.add_argument(
        "--assets_dir",
        "-a",
        type=Path,
        required=False,
        default="assets",
        help="Directory to store repository assets.",
    )

    args = parser.parse_args()
    return args


async def main() -> None:
    """
    Main coordinates the flow of proposed data through our normalization
    functions defined in the library `normalize.py`.
    """
    args = parse_command_line_args()

    # make sure the input table path points to a file that exists
    assert os.path.isfile(
        args.input_table
    ), f"The provided file {args.input_table} does not exist."

    # scan in the TSV
    table_df = pl.scan_csv(args.input_table, separator="\t")

    # make sure all asset files are present
    await validate_asset_files(table_df, args.assets_dir)

    # remove duplicate rows while any validation finishes
    normalized_df = await remove_duplicate_rows(table_df)

    # write out the final CSV
    normalized_df.sink_csv("normalized_table.tsv", separator="\t")


if __name__ == "__main__":
    print(GIT_MILK_BANNER)
    asyncio.run(main())
