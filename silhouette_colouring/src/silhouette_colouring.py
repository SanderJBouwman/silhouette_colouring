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
from PIL import Image
from silhouette_colouring.src.utils import load_csv_file, parse_arguments


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

    darkened = tuple(
        [int(value * (1 - factor)) for value in (red, green, blue)])
    return darkened[0], darkened[1], darkened[2]


def change_color(input_image: Image.Image,
                 hex_code: str,
                 darken_factor: float = 0.2
                 ) -> Image.Image:
    """
    Change the color of the image to the given hex code and return a new image
    :param darken_factor:  Factor to darken the color by (0-1)
    :param input_image: Image to change the color of
    :param hex_code: Hex code to change the color to (e.g. #FF0000)
    :return:  New image with the changed color
    """
    data: np.ndarray = np.array(input_image)

    current_light: tuple[int, int, int, int] = (128, 128, 255, 255)
    new_light: np.ndarray = np.append(hex_to_rgb(hex_code), 255)

    # Create the new_dark which is the same as the new_light but darker by 10%
    current_dark: tuple[int, int, int, int] = (0, 0, 255, 255)

    new_dark: np.ndarray = np.append(
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


def discover_files(target_dir: Path, search_query: str):
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
                 darkening_factor: float) -> None:
    """
    Process a file by changing the color of the GIF and saving it to the output
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

    original_image: Image.Image = Image.open(filepath).convert('RGBA')
    colored_image: Image.Image = change_color(original_image,
                                              row["color"].iloc[0],
                                              darkening_factor)

    cluster = str(row["cluster"].iloc[0])
    gif_filename: str = Path(filepath).name.replace("-sil",
                                                    "-colored").replace(
        " ", "_")
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

    n_processes: int = mp.cpu_count()
    with mp.Pool(n_processes) as pool:
        pool.starmap(process_file,
                     [(filepath, color_csv_df, args.outputDir, args.darkening)
                      for filepath in filepaths])

    return 0


if __name__ == '__main__':
    sys.exit(main())
