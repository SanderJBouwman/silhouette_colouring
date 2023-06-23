#!usr/bin/env python
"""
This is the main script for the silhouette colouring project. It takes a
silhouette image and changes the colour of the silhouette to the given hex
code. It then saves the new image to the output directory.
"""
import argparse
import multiprocessing as mp
import sys
import time
from pathlib import Path

import pandas as pd
import tqdm

from silhouette_colouring.src.utils import (
    load_csv_file,
    parse_arguments,
    discover_files,
    recolour_file,
)


def main() -> int:
    start_time = time.time()

    args: argparse.Namespace = parse_arguments()
    gif_input_dir: Path = args.gif_input_dir
    input_csv: Path = args.input_csv

    color_csv_df: pd.DataFrame = load_csv_file(input_csv)
    filepaths: list[Path] = discover_files(gif_input_dir, "*.gif")

    if len(filepaths) == 0:
        raise FileNotFoundError(f"No GIFs found in {gif_input_dir}")

    n_processes: int = mp.cpu_count()
    progress_bar: tqdm.tqdm = tqdm.tqdm(
        total=len(filepaths), desc="Processing GIFs", unit="GIFs"
    )

    def update_progress(*_: object) -> None:
        progress_bar.update()

    was_successful: list = []
    with mp.Pool(n_processes) as pool:
        results = [
            pool.apply_async(
                recolour_file,
                (
                    filepath,
                    color_csv_df,
                    args.output,
                    args.darkening,
                    args.light_colour,
                    args.dark_colour,
                    args.discover_colours,
                    args.verbose,
                ),
                callback=update_progress,
            )
            for filepath in filepaths
        ]

        # Wait for all processes to complete
        for result in results:
            was_successful.append(result.get())

    progress_bar.close()

    processing_time: float = round(time.time() - start_time, 2)
    print(
        f"Processed {was_successful.count(0)}/{len(was_successful)} "
        f"GIFs succesfully (in {processing_time} seconds)",
        end="",
    )

    if was_successful.count(0) != len(was_successful):
        print(
            "| "
            f"cell_ID not found in CSV: {was_successful.count(1)} "
            f"images, "
            f"light colour not found: {was_successful.count(2)} images, "
            f"dark colour not found: {was_successful.count(3)} images"
        )
        if not args.verbose:
            print(
                "Try running the script with the --verbose flag to see which "
                "images failed to process."
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())

__all__ = []
