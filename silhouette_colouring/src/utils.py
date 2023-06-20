#!usr/bin/env python
"""
This module contains utility functions for the silhouette colouring project.
"""
import argparse
import sys
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

    parser.add_argument("--light-colour", type=str,
                        metavar="R,G,B[,A]",
                        default=None,
                        help="Specify the light colour as 3 or 4 comma-separated integers (RGB or RGBA). "
                             "Example: 128,128,255 or 128,128,255,255. "
                             "Default: 128,128,255.")

    parser.add_argument("--dark-colour", type=str,
                        metavar="R,G,B[,A]",
                        default=None,
                        help="Specify the dark colour as 3 or 4 "
                             "comma-separated integers (RGB or RGBA)."
                             "Example: 0,0,255 or 0,0,255,255. Default: 0,0,255.")

    parser.add_argument("--discover-colours", action="store_true",
                        default=False,
                        help="Will discover the light and "
                             "dark colours from the image. "
                             "The second most used color will be assigned "
                             "to --light-colour and the third"
                             " most used color will "
                             "be assigned to --dark-colour. "
                             "This will override the --dark-colour "
                             "and --light-colour values")

    parser.add_argument("--verbose", "-v", action="store_true",
                        default=False,
                        help="Print more information to the console")

    args = parser.parse_args()
    validate_args(args)
    return args


def parse_colour(colour_str: str) -> tuple[int, int, int, int]:
    colour_values = colour_str.split(",")
    if len(colour_values) not in [3, 4]:
        raise argparse.ArgumentTypeError(
            "Colour must be specified as 3 or 4 "
            "comma-separated integers (RGB or RGBA).")
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

    # We need to specify both light_colour and dark_colour if we want to
    # override the colour discovery step
    default_light_colour = "128,128,255,255"
    default_dark_colour = "0,0,255,255"
    if args.discover_colours:
        print("WARNING: Using colour discovery. This will override the "
              "light_colour and dark_colour arguments.", file=sys.stderr)

    if args.light_colour is not None or args.dark_colour is not None:
        if args.discover_colours:
            raise ValueError("You cannot specify both --discover-colours and "
                             "--light-colour/--dark-colour at the same time. "
                             "This is because using --discover-colours  will "
                             "overwrite --light-colour and --dark-colour "
                             "making them redundant.")

    if args.light_colour is None and args.discover_colours is False:
        args.light_colour = parse_colour(default_light_colour)
        print(
            f"WARNING: You have not specified a light colour. Using default: {args.light_colour}", file=sys.stderr)
    elif args.light_colour is not None and args.discover_colours is False:
            args.light_colour = parse_colour(args.light_colour)

    if args.dark_colour is None and args.discover_colours is False:
        args.dark_colour = parse_colour(default_dark_colour)
        print(f"WARNING: You have not specified a dark colour. Using default: {args.dark_colour}", file=sys.stderr)
    elif args.dark_colour is not None and args.discover_colours is False:
        args.dark_colour = parse_colour(args.dark_colour)





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
