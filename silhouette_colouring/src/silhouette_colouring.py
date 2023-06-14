#!usr/bin/env python3
from PIL import Image
import numpy as np
import colorsys
from pathlib import Path
import pandas as pd
import struct
import argparse
import multiprocessing as mp
from silhouette_colouring.src.utils import validate_args, load_csv_file

"""
How to use:
Run the help command to see the arguments 
python3 SilhouetteColoringGIF.py -h
"""


def adjust_color_lightness(r: int, g: int, b: int, factor: float) -> tuple[
    int, int, int]:
    # Convert RGB to HLS
    h: float
    l: float
    s: float

    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # We use max and min to make sure that the value is between 0 and 1
    l = max(min(l * factor, 1.0), 0.0)

    # We use map to convert the values to ints
    r, g, b = map(int, colorsys.hls_to_rgb(h, l, s))
    return int(r * 255), int(g * 255), int(b * 255)


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    rgb = struct.unpack("BBB", bytes.fromhex(hex_code.lstrip("#")))
    if len(rgb) != 3:
        raise ValueError("Invalid hex code")

    return tuple[int, int, int](rgb)


def darken_color(r: int, g: int, b: int, factor: float = 0.1) -> tuple[
    int, int, int]:
    darkened = tuple([int(value * (1 - factor)) for value in (r, g, b)])
    return darkened


def change_color(im: Image.Image, hex_code: str,
                 darken_factor: float = 0.2) -> Image.Image:
    """
    Change the color of the image to the given hex code and return a new image
    :param im: Image to change the color of
    :param hex_code: Hex code to change the color to (e.g. #FF0000)
    :return:  New image with the changed color
    """
    data: np.ndarray = np.array(im)

    current_light = (128, 128, 255, 255)
    new_light = hex_to_rgb(hex_code)
    new_light = np.append(new_light, 255)

    # Create the new_dark which is the same as the new_light but darker by 10%
    current_dark = (0, 0, 255, 255)
    new_dark = [int(value * (1 - darken_factor)) for value in new_light[:3]]
    new_dark = np.append(new_dark, 255)

    # Replace the current_light with the new_light and current_dark with the new_dark
    data[(data == current_light).all(axis=2)] = new_light
    data[(data == current_dark).all(axis=2)] = new_dark

    # Create a new image from the data
    new_im: Image.Image = Image.fromarray(data, mode="RGBA")
    return new_im


def process_line(line: pd.Series, gif_dir, output_dir,
                 darkening_factor) -> None:
    # Find a file with the same name as the cell_ID

    res = gif_dir.glob(str(line["cell_ID"]) + "*")

    # Check the result
    res = list(res)

    if res is None or len(res) == 0:
        return

    input_gif_path: str = list(res)[0]

    im: Image.Image = Image.open(input_gif_path).convert('RGBA')
    colored = change_color(im, line["color"], darkening_factor)

    cluster = str(line["cluster"])
    gif_filename: str = Path(input_gif_path).name.replace("-sil",
                                                          "-colored").replace(
        " ", "_")
    output_gif_path: Path = output_dir / (cluster + "_" + gif_filename)

    # Save colored image
    colored.save(output_gif_path, format='GIF', save_all=True,
                 append_images=[colored])

    colored.close()


def parse_arguments():
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
        help="Darkening factor (default: 0.2)",
    )
    parser.add_argument(
        "--outputDir",
        "-o",
        type=Path,
        required=False,
        help="Output directory (default: gif_input_dir/output)",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    validate_args(args)

    # Return the argument values
    return args


def csv_is_valid(df: pd.DataFrame) -> (bool, list[str]):
    valid = True
    missing_columns = []
    needed_columns = ["cell_ID", "cluster", "color"]

    for column in needed_columns:
        if column not in df.columns:
            valid = False
            missing_columns.append(column)

    return valid, missing_columns


def discover_files(target_dir: Path, search_query: str):
    """
    Discover files in a directory with a search query.

    :param target_dir: The directory to search in.
    :param search_query: The search query to use. This can be a glob pattern.
    #
    :return: A list of paths to files that match the search query.
    """
    return list(target_dir.glob(search_query))


def process_file(filepath: Path, reference_df: pd.DataFrame, output_dir: Path,
                 darkening_factor: float):
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


def main(args):
    gif_input_dir: Path = args.gif_input_dir
    input_csv: Path = args.input_csv

    color_csv_df: pd.DataFrame = load_csv_file(input_csv)
    filepaths: list[Path] = discover_files(gif_input_dir, "*.gif")

    if len(filepaths) == 0:
        print("No GIFs found")
        exit(0)

    n_processes = mp.cpu_count()
    # Now we'll create the pool of processes
    pool = mp.Pool(n_processes)
    # And pass the chunks to the pool of processes
    pool.starmap(process_file,
                 [(filepath, color_csv_df, args.outputDir, args.darkening) for
                  filepath in filepaths])
    # Close the pool to prevent any more tasks from being submitted to the pool
    pool.close()
    # Wait for the worker processes to exit
    pool.join()

    print("Done")
    exit(0)


if __name__ == '__main__':
    args = parse_arguments()
    exit(main(args))
