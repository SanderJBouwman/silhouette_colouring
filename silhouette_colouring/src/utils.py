#!usr/bin/env python
"""
This module contains utility functions for the silhouette colouring project.
"""
import argparse
import struct
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from PIL import Image

from silhouette_colouring.src.validators import validate_args


def parse_arguments() -> argparse.Namespace:  # pragma: no cover
    """
    Parse the command-line arguments and return the values.
    :return: The command-line arguments (as a Namespace object)
    """
    # Create the parser
    parser = argparse.ArgumentParser(description="Change color of GIFs")

    # Add the command-line arguments
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to CSV file. "
        "The CSV must have "
        "the following columns: "
        "`cell_ID`, `cluster` "
        "and `color`",
    )

    parser.add_argument(
        "gif_input_dir", type=Path, help="Path where the GIFs are located"
    )
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

    parser.add_argument(
        "--light-colour",
        type=str,
        metavar="R,G,B[,A]",
        default=None,
        help="Specify the light colour as 3 or 4 "
        "comma-separated integers (RGB or RGBA). "
        "Example: 128,128,255 or 128,128,255,255. "
        "Default: 128,128,255.",
    )

    parser.add_argument(
        "--dark-colour",
        type=str,
        metavar="R,G,B[,A]",
        default=None,
        help="Specify the dark colour as 3 or 4 "
        "comma-separated integers (RGB or RGBA)."
        "Example: 0,0,255 or 0,0,255,255. "
        "Default: 0,0,255.",
    )

    parser.add_argument(
        "--discover-colours",
        action="store_true",
        default=False,
        help="Will discover the light and "
        "dark colours from the image. "
        "The second most used color will be assigned "
        "to --light-colour and the third"
        " most used color will "
        "be assigned to --dark-colour. "
        "This will override the --dark-colour "
        "and --light-colour values",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Print more information to the console",
    )

    args = parser.parse_args()
    validate_args(args)
    return args


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
            f"CSV file '{path}' is missing the following columns: " f"{missing_columns}"
        )

    # Return the DataFrame
    return loaded_csv_df


def discover_colours(
    image: Image.Image,
) -> tuple[[int, int, int, int], [int, int, int, int]]:
    """
    Discover the light and dark colours of the image by using the 'getcolors'
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


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """
    Convert a hex code to an RGB tuple using the struct library
    :param hex_code: Hex code to convert to RGB (e.g. #FF0000)
    :return: RGB tuple
    """
    rgb = struct.unpack("BBB", bytes.fromhex(hex_code.lstrip("#")))
    return rgb[0], rgb[1], rgb[2]


def darken_color(
    red: int, green: int, blue: int, factor: float = 0.1
) -> tuple[int, int, int]:
    """
    Darken the given color by the given factor and return the new color as a
    tuple
    :param red: value (0-255)
    :param green: value (0-255)
    :param blue: value (0-255)
    :param factor: Factor to darken the color by (0-1)
    :return:
    """
    if (
        not isinstance(red, int)
        or not isinstance(green, int)
        or not isinstance(blue, int)
    ):
        raise TypeError(f"Parameters red, green and blue must be integers")

    if not all(0 <= x <= 255 for x in [red, green, blue]):
        raise ValueError("Red, green and blue must be between 0 and 255")

    if factor < 0 or factor > 1:
        raise ValueError("Factor must be between 0 and 1")
    darkened_red = int(red * (1 - factor))
    darkened_green = int(green * (1 - factor))
    darkened_blue = int(blue * (1 - factor))
    return darkened_red, darkened_green, darkened_blue


def change_color(
    input_image: Image.Image,
    hex_code: str,
    darken_factor: float = 0.2,
    current_light: tuple[int, int, int, int] = (128, 128, 255, 255),
    current_dark: tuple[int, int, int, int] = (0, 0, 255, 255),
) -> Image.Image:
    """
    Change the color of the image to the given hex code and return a new image
    :param current_dark:  The current color of the image (dark) that will be
    changed to the new color
    :param current_light: The current color of the image (light) that will be
    changed to the new color
    :param darken_factor:  Factor to darken the color by (0-1)
    :param input_image: Image to change the color of
    :param hex_code: Hex code to change the color to (e.g. #FF0000)
    :return:  New image with the changed color
    """
    data: np.ndarray[np.uint8] = np.array(input_image)

    new_light: np.ndarray[np.uint8] = np.append(hex_to_rgb(hex_code), 255)

    # Create the new_dark which is the same as the new_light but darker by 10%
    new_dark: np.ndarray[np.uint8] = np.append(
        darken_color(
            int(new_light[0]), int(new_light[1]), int(new_light[2]), darken_factor
        ),
        255,
    )

    # Replace the current_light with the new_light and current_dark with the
    # new_dark
    data[(data == current_light).all(axis=2)] = new_light
    data[(data == current_dark).all(axis=2)] = new_dark

    # Create a new image from the data
    new_im: Image.Image = Image.fromarray(data, mode="RGBA")

    return new_im


def discover_files(target_dir: Path, search_query: str) -> list[Path]:
    """
    Discover files in a directory with a search query.

    :param target_dir: The directory to search in.
    :param search_query: The search query to use. This can be a glob pattern.
    #
    :return: A list of paths to files that match the search query.
    """
    return list(target_dir.glob(search_query))


def recolour_file(
    filepath: Path,
    reference_df: pd.DataFrame,
    output_dir: Path,
    darkening_factor: float,
    light_colour: tuple[int, int, int, int],
    dark_colour: tuple[int, int, int, int],
    discover_colour: bool,
    run_verbose: bool,
) -> int:  # pragma: no cover
    """
    Process a file by changing the color of the GIF and saving it to the output
    :param run_verbose: Run verbose mode (which shows more information)
    :param discover_colour: Discover the colour of the GIF
    :param dark_colour: RGBA tuple of the dark colour to use when changing the
    color of the GIF
    :param light_colour: RGBA tuple of the light colour to use when changing
    the color of the GIF
    :param filepath: filepath to the GIF
    :param reference_df: reference dataframe that will be used to change the
    color of the GIF
    :param output_dir: output directory where the GIF will be saved
    :param darkening_factor: darkening factor to use when
    changing the color of the nucleus
    :return: Exit code: 0 = success, 1 = cell_ID not found in reference_df,
    2 = light colour not in image, 3 = dark colour not in image

    """

    # Find the row in the reference_df
    row: pd.Series = reference_df.loc[reference_df["cell_ID"] == filepath.stem]

    # Check if the row exists
    if len(row) == 0:
        if run_verbose:
            print(
                f"WARNING: Skipping image ({filepath.name}) due to: "
                f"cell_ID not found in CSV",
                file=sys.stderr,
            )
        return 1

    original_image: Image.Image = Image.open(filepath).convert("RGBA")
    if discover_colour:
        light_colour, dark_colour = discover_colours(original_image)
        if run_verbose:
            print(
                f"INFO: Discovered light colour (RGBA): {light_colour} "
                f"and dark colour (RGBA): {dark_colour} for image: {filepath.name}"
            )

    # Get the colors from the original image
    colours = [x[1] for x in original_image.getcolors(256)]
    # Check if the light and dark colours are in the original image
    if light_colour not in colours:
        if run_verbose:
            print(
                f"WARNING: Skipping image ({filepath.name}) due to: "
                f"Light colour {light_colour} not in image",
                file=sys.stderr,
            )
        return 2

    if dark_colour not in colours:
        if run_verbose:
            print(
                f"WARNING: Skipping image ({filepath.name}) due to: "
                f"Dark colour {dark_colour} not in image",
                file=sys.stderr,
            )
        return 3

    colored_image: Image.Image = change_color(
        original_image,
        row["color"].iloc[0],
        darkening_factor,
        light_colour,
        dark_colour,
    )

    cluster = str(row["cluster"].iloc[0])
    gif_filename: str = filepath.name.replace("-sil", "-colored").replace(" ", "_")

    output_gif_path: Path = output_dir / (cluster + "_" + gif_filename)

    # Save colored image
    colored_image.save(output_gif_path, format="GIF")

    original_image.close()
    colored_image.close()

    return 0


__all__ = [
    "parse_arguments",
    "load_csv_file",
    "discover_colours",
    "hex_to_rgb",
    "darken_color",
    "change_color",
    "discover_files",
    "recolour_file",
]
