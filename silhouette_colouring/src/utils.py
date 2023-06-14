#!usr/bin/env python
"""
This module contains utility functions for the silhouette colouring project.
"""
import argparse
from pathlib import Path

import pandas as pd


def parse_arguments() -> argparse.Namespace:
    """
    Parse the command-line arguments and return the values.
    :return: The command-line arguments (as a Namespace object)
    """
    # Create the parser
    parser = argparse.ArgumentParser(description="Change color of GIFs")

    # Add the command-line arguments
    parser.add_argument("input_csv", type=Path, help="Path to CSV file")
    parser.add_argument("gif_input_dir", type=Path,
                        help="Path where the GIFs are located")
    parser.add_argument(
        "--darkening",
        "-d",
        type=float,
        default=0.2,
        help="Darkening factor (default: 0.2) - must be between 0.0 and 1.0",
    )
    parser.add_argument(
        "--outputDir",
        "-o",
        type=Path,
        required=False,
        help="Output directory (default: gif_input_dir/output)",
    )

    args = parser.parse_args()
    validate_args(args)
    return args


def validate_args(args):
    """
    Validate the arguments. This function will raise an exception if the
    arguments are invalid. If the arguments are valid, nothing will happen.
    :param args: The arguments to validate
    :return: None
    """
    # Validate paths
    if not args.input_csv.exists():
        raise FileNotFoundError(
            f"CSV path '{args.input_csv}' "
            f"does not exist. Are you sure this is the right location?")

    # input_csv should be a csv file
    if args.input_csv.suffix != ".csv":
        raise ValueError(f"Input CSV '{args.input_csv}' "
                         f"is not a CSV file")

    if not args.gif_input_dir.exists():
        raise FileNotFoundError(
            f"GifInputDir path '{args.gif_input_dir}' "
            f"does not exist. Are you sure this is the right location")

    if args.outputDir is None:
        args.outputDir = args.gif_input_dir / "SilhouetteOutput"
        print(
            f"No output directory specified. Using default '{args.outputDir}'")

    if not args.outputDir.exists():
        args.outputDir.mkdir()

    # Validate darkening factor
    if args.darkening < 0 or args.darkening > 1:
        raise ValueError(
            f"Darkening factor '{args.darkening}' must be between 0.0 and 1.0")

def csv_is_valid(loaded_csv_df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Check if the CSV file is valid by checking if it has the needed columns.
    :param loaded_csv_df: The dataframe to check
    :return: A tuple with a boolean and a list of missing columns
    """
    valid: bool = True
    missing_columns: list[str] = []
    needed_columns: list[str] = ["cell_ID", "cluster", "color"]

    for column in needed_columns:
        if column not in loaded_csv_df.columns:
            valid = False
            missing_columns.append(column)

    return valid, missing_columns





def load_csv_file(path: Path) -> pd.DataFrame:
    """
    Load the CSV file and return a DataFrame
    :param path: Path to the CSV file
    :return: DataFrame
    """

    # Read the CSV file
    loaded_csv_df: pd.DataFrame = pd.read_csv(path)

    # Validate the CSV file
    if len(loaded_csv_df) == 0:
        raise ValueError(f"CSV file '{path}' is empty")

    # Check if it has the required columns
    valid, missing_columns = csv_is_valid(loaded_csv_df)
    if not valid:
        raise ValueError(
            f"CSV file '{path}' is missing the following columns: "
            f"{missing_columns}")

    # Return the DataFrame
    return loaded_csv_df
