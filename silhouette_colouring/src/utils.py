#!usr/bin/env python
"""
This module contains utility functions for the silhouette colouring project.
"""
import argparse
from pathlib import Path

import pandas as pd
from PIL import Image


def parse_arguments() -> argparse.Namespace:
    """
    Parse the command-line arguments and return the values.
    :return: The command-line arguments (as a Namespace object)
    """
    # Create the parser
    parser = argparse.ArgumentParser(description="Change color of GIFs")

    # Add the command-line arguments
    parser.add_argument("input_csv", type=Path, help="Path to CSV file. "
                                                     "The CSV must have "
                                                     "the following columns: "
                                                     "`cell_ID`, `cluster` "
                                                     "and `color`")

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
        "--output",
        "-o",
        type=Path,
        required=False,
        help="Output directory (default: working directory)",
    )

    parser.add_argument("--light-colour", type=parse_colour,
                        metavar="R,G,B[,A]",
                        default="128,128,255",
                        help="Specify the light colour as 3 or 4 comma-separated integers (RGB or RGBA). "
                             "Example: 128,128,255 or 128,128,255,255. "
                             "Default: 128,128,255.")

    parser.add_argument("--dark-colour", type=parse_colour,
                        metavar="R,G,B[,A]",
                        default="0,0,255",
                        help="Specify the dark colour as 3 or 4 "
                             "comma-separated integers (RGB or RGBA)."
                             "Example: 0,0,255 or 0,0,255,255. Default: 0,0,255.")

    parser.add_argument("--no-discover-colours", action="store_false",
                        default=True,
                        help="Will remove the colour discovery step and and "
                             "uses the --light-colour and --dark-colour")

    args = parser.parse_args()
    validate_args(args)
    return args


def parse_colour(colour_str: str) -> tuple[int, int, int, int]:
    colour_values = colour_str.split(",")
    if len(colour_values) not in [3, 4]:
        raise argparse.ArgumentTypeError(
            "Colour must be specified as 3 or 4 comma-separated integers (RGB or RGBA).")
    try:
        colour_ints = [int(val) for val in colour_values]
        if any(val < 0 or val > 255 for val in colour_ints):
            raise argparse.ArgumentTypeError(
                "Colour values must be in the range of 0-255.")
    except ValueError:
        raise argparse.ArgumentTypeError("Colour values must be integers.")

    if len(colour_ints) == 3:
        alpha: int = 255
    else:
        alpha: int = colour_ints[3]

    return colour_ints[0], colour_ints[1], colour_ints[2], alpha


def validate_args(args: argparse.Namespace) -> None:
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
            f"does not exist. Are you sure this is the right location?")

    if args.output is None:
        # We set the output to the current working directory
        args.output = Path.cwd()

    if not args.output.exists():
        raise FileNotFoundError(
            f"Output path '{args.output}' "
            f"does not exist. Are you sure this is the right location?")

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


def discover_colours(image: Image.Image) -> tuple[
    [int, int, int, int], [int, int, int, int]]:
    """
    Discover the light and dark colours of the image by using the getcolors
    method of the Image class. We expect that the light colour is the second
    most common colour and the dark colour is the third most common colour.
    :param image: The image to discover the colours of (PIL Image)
    :return: A tuple with the light and dark colours as RGBA tuples
    """
    colours: list[tuple] = image.getcolors(256)
    colours: list[tuple] = sorted(colours, key=lambda x: x[0], reverse=True)

    light_colour: tuple[int, int, int, int] = colours[1][1]
    dark_colour: tuple[int, int, int, int] = colours[2][1]
    return light_colour, dark_colour


__all__ = ["parse_arguments", "load_csv_file", "discover_colours"]
