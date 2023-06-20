#!usr/bin/env python
"""
This is the main script for the silhouette colouring project. It takes a
silhouette image and changes the colour of the silhouette to the given hex
code. It then saves the new image to the output directory.
"""
import argparse
import multiprocessing as mp
import struct
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import tqdm
from PIL import Image

from silhouette_colouring.src.utils import load_csv_file, parse_arguments, \
    discover_colours


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """
    Convert a hex code to a RGB tuple using the struct library
    :param hex_code: Hex code to convert to RGB (e.g. #FF0000)
    :return: RGB tuple
    """
    rgb = struct.unpack("BBB", bytes.fromhex(hex_code.lstrip("#")))
    if len(rgb) != 3:
        raise ValueError("Invalid hex code")

    return rgb[0], rgb[1], rgb[2]


def darken_color(red: int,
                 green: int,
                 blue: int,
                 factor: float = 0.1) -> \
        tuple[int, int, int]:
    """
    Darken the given color by the given factor and return the new color as a
    tuple
    :param red: value (0-255)
    :param green: value (0-255)
    :param blue: value (0-255)
    :param factor: Factor to darken the color by (0-1)
    :return:
    """
    if factor < 0 or factor > 1:
        raise ValueError("Factor must be between 0 and 1")
    darkened_red = int(red * (1 - factor))
    darkened_green = int(green * (1 - factor))
    darkened_blue = int(blue * (1 - factor))
    return darkened_red, darkened_green, darkened_blue


def change_color(input_image: Image.Image,
                 hex_code: str,
                 darken_factor: float = 0.2,
                 current_light: tuple[int, int, int, int] = (
                         128, 128, 255, 255),
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
            new_light[0],
            new_light[1],
            new_light[2],
            darken_factor
        ), 255)

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


def process_file(filepath: Path,
                 reference_df: pd.DataFrame,
                 output_dir: Path,
                 darkening_factor: float,
                 light_colour: tuple[int, int, int, int],
                 dark_colour: tuple[int, int, int, int],
                 use_discover_colour: bool) -> None:
    """
    Process a file by changing the color of the GIF and saving it to the output
    :param use_discover_colour:
    :param dark_colour:
    :param light_colour:
    :param filepath: filepath to the GIF
    :param reference_df: reference dataframe that will be used to change the
    color of the GIF
    :param output_dir: output directory where the GIF will be saved
    :param darkening_factor: darkening factor to use when
    changing the color of the nucleus
    :return: None
    """

    # Find the row in the reference_df
    row: pd.Series = reference_df.loc[reference_df["cell_ID"] == filepath.stem]

    # Check if the row exists
    if len(row) == 0:
        return

    original_image: Image.Image = Image.open(filepath).convert("RGBA")
    if use_discover_colour:
        print(f"Discovering colours for {filepath}")
        light_colour, dark_colour = discover_colours(original_image)

    colored_image: Image.Image = change_color(original_image,
                                              row["color"].iloc[0],
                                              darkening_factor,
                                              light_colour,
                                              dark_colour)

    cluster = str(row["cluster"].iloc[0])
    gif_filename: str = filepath.name. \
        replace("-sil", "-colored").replace(" ", "_")

    output_gif_path: Path = output_dir / (cluster + "_" + gif_filename)

    # Save colored image
    colored_image.save(output_gif_path, format="GIF")

    original_image.close()
    colored_image.close()

def main() -> int:
    args: argparse.Namespace = parse_arguments()
    gif_input_dir: Path = args.gif_input_dir
    input_csv: Path = args.input_csv

    color_csv_df: pd.DataFrame = load_csv_file(input_csv)
    filepaths: list[Path] = discover_files(gif_input_dir, "*.gif")

    if len(filepaths) == 0:
        print("No GIFs found")
        sys.exit(0)

    if args.no_discover_colours == False:
        print(f"Discover mode is turned off. Using colours from "
              f"--light-colour {args.light_colour} and --dark-co"
              f"lour {args.dark_colour}")
    else:
        print("Discovering mode is turned on. Using colours from GIFs")

    n_processes: int = mp.cpu_count()
    progress_bar: tqdm.tqdm = tqdm.tqdm(total=len(filepaths),
                                        desc="Processing GIFs",
                                        unit="GIFs")

    def update_progress(*_: object) -> None:
        progress_bar.update()

    with mp.Pool(n_processes) as pool:
        results = [
            pool.apply_async(process_file, (
                filepath, color_csv_df, args.output, args.darkening,
                args.light_colour, args.dark_colour, args.no_discover_colours),
                             callback=update_progress)
            for filepath in filepaths
        ]

        # Wait for all processes to complete
        for result in results:
            result.get()

    progress_bar.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())

__all__ = ["change_color", "process_file"]
