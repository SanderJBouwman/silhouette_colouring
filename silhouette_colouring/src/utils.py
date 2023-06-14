from pathlib import Path

import pandas as pd


def validate_args(args):
    # Validate paths
    if not args.input_csv.exists():
        raise FileNotFoundError(
            f"CSV path '{args.input_csv}' does not exist. Are you sure this is the right location?")

    # input_csv should be a csv file
    if args.input_csv.suffix != ".csv":
        raise ValueError(f"Input CSV '{args.input_csv}' is not a CSV file")

    if not args.gif_input_dir.exists():
        raise FileNotFoundError(
            f"GifInputDir path '{args.gif_input_dir}' does not exist. Are you sure this is the right location")

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


def load_csv_file(path: Path) -> pd.DataFrame:
    """
    Load the CSV file and return a DataFrame
    :param path: Path to the CSV file
    :return: DataFrame
    """

    # Read the CSV file
    df: pd.DataFrame = pd.read_csv(path)

    # Validate the CSV file
    if len(df) == 0:
        raise ValueError(f"CSV file '{path}' is empty")

    # Check if it has the required columns
    valid, missing_columns = csv_is_valid(df)
    if not valid:
        raise ValueError(
            f"CSV file '{path}' is missing the following columns: "
            f"{missing_columns}")

    # Return the DataFrame
    return df
