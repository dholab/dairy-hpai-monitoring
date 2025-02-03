#!/usr/bin/env python3

"""
usage: splice_readme.py [-h] [-r README] [-f TALLY_FILE]

Space a table from one input markdown file into the README.

options:
  -h, --help            show this help message and exit
  -r README, --readme README
                        The readme to be updated.
  -f TALLY_FILE, --tally_file TALLY_FILE
                        The file to be spliced into the readme.
"""

import argparse
from io import TextIOWrapper
from pathlib import Path
from typing import List


def parse_command_line_args() -> argparse.Namespace:
    """
    Parse a couple named arguments from the command line
    """
    parser = argparse.ArgumentParser(
        description="Space a table from one input markdown file into the README.",
    )
    parser.add_argument(
        "-r",
        "--readme",
        type=Path,
        default=Path("README.md"),
        required=False,
        help="The readme to be updated.",
    )
    parser.add_argument(
        "-f",
        "--tally_file",
        type=Path,
        default=Path("assets/positivity_tally.md"),
        required=False,
        help="The file to be spliced into the readme.",
    )

    return parser.parse_args()


def splice_readme_lines(
    readme_lines: list[str],
    tally_lines: list[str],
    new_readme: TextIOWrapper,
) -> None:
    """
    Test a few conditions on each line to make sure the tally table is properly
    spliced into the readme.
    """
    ignore = False
    for line in readme_lines:
        if line.startswith("## All-time Results by State"):
            new_readme.write("## All-time Results by State\n\nFull results across the history of the project (24 April 2024-Present)\n")
            for tally_line in tally_lines:
                new_readme.write(f"{tally_line}")
            ignore = True

        if line.startswith("## Sampling Dairy Products for HPAI RNA"):
            new_readme.write("\n")
            ignore = False

        if not ignore:
            new_readme.write(f"{line}")
            continue


def main() -> None:
    """
    Script entrypoint
    """

    # parse out command line args
    args = parse_command_line_args()

    # open the input readme and tally md file and collect the lines from each
    with open(args.readme, encoding="utf8") as readme_handle:
        readme_lines = list(readme_handle.readlines())
    with open(args.tally_file, encoding="utf8") as tally_handle:
        tally_lines = list(tally_handle.readlines())

    # open the new readme and handle splicing the table into the new readme
    with open("new_readme.md", "w", encoding="utf8") as new_readme:
        splice_readme_lines(readme_lines, tally_lines, new_readme)


if __name__ == "__main__":
    main()
