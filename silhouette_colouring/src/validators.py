import argparse
import sys
from pathlib import Path


def validate_input_csv(input_csv: Path) -> None:
    if not input_csv.exists():
        raise FileNotFoundError(
            f"CSV path '{input_csv}' "
            f"does not exist. Are you sure this is the right location?"
        )

    # input_csv should be a csv file
    if input_csv.suffix != ".csv":
        raise ValueError(f"Input CSV '{input_csv}' " f"is not a CSV file")


def validate_gif_input_dir(gif_input_dir: Path) -> None:
    if not gif_input_dir.exists():
        raise FileNotFoundError(
            f"GifInputDir path '{gif_input_dir}' "
            f"does not exist. Are you sure this is the right location?"
        )

    # gif_input_dir should be a directory
    if not gif_input_dir.is_dir():
        raise ValueError(f"GifInputDir '{gif_input_dir}' " f"is not a directory")

    # gif_input_dir should contain at least one GIF
    if len(list(gif_input_dir.glob("*.gif"))) == 0:
        raise ValueError(f"GifInputDir '{gif_input_dir}' " f"does not contain any GIFs")


def validate_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        raise FileNotFoundError(
            f"Output path '{output_dir}' "
            f"does not exist. Are you sure this is the right location?"
        )

    # output_dir should be a directory
    if not output_dir.is_dir():
        raise ValueError(f"Output '{output_dir}' " f"is not a directory")


def validate_darkening_factor(darkening_factor: float | int) -> None:
    if not isinstance(darkening_factor, (float, int)):
        raise TypeError(
            f"Darkening factor '{darkening_factor}' " f"must be a float or an int"
        )

    if darkening_factor < 0 or darkening_factor > 1:
        raise ValueError(
            f"Darkening factor '{darkening_factor}' must be between " f"0.0 and 1.0"
        )


def validate_input_colour(light_colour: str | None) -> None:
    # Must be a string or None
    if not isinstance(light_colour, (str, type(None))):
        raise TypeError(f"Light colour '{light_colour}' " f"must be a string or None")

    if light_colour is None:
        return

    try:
        parse_colour(light_colour)
    except argparse.ArgumentTypeError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid light colour '{light_colour}'. " f"{e}"
        )


def validate_replacement_colour(
    replacement_colour: str,
    discover_colours: bool,
    default_color: str,
    argument_name: str,
) -> tuple[int, int, int, int] | None:
    if discover_colours and replacement_colour is not None:
        raise argparse.ArgumentTypeError(
            "You cannot specify both --discover-colours and "
            "--light-colour/--dark-colour at the same time. "
            "This is because using --discover-colours  will "
            "overwrite --light-colour and --dark-colour "
            "making them redundant."
        )

    if discover_colours and replacement_colour is None:
        return None

    if not discover_colours and replacement_colour is None:
        print(
            f"Warning: Argument {argument_name} not specified. "
            f"Using default colour: {default_color}.",
            file=sys.stderr,
        )
        return parse_colour(default_color)

    if replacement_colour is not None:
        return parse_colour(replacement_colour)


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate the arguments. This function will raise an exception if the
    arguments are invalid. If the arguments are valid, nothing will happen.
    :param args: The arguments to validate
    :return: None
    """
    # Validate paths

    validate_input_csv(args.input_csv)

    validate_gif_input_dir(args.gif_input_dir)

    # We set the output to the current working directory if it is not
    # specified.
    if args.output is None:
        args.output = Path.cwd()

    validate_output_dir(args.output)

    validate_darkening_factor(args.darkening)

    # Validate colours
    validate_input_colour(args.light_colour)
    validate_input_colour(args.dark_colour)

    # We need to specify both light_colour and dark_colour if we want to
    # override the colour discovery step
    default_light_colour = "128,128,255,255"
    default_dark_colour = "0,0,255,255"

    args.light_colour = validate_replacement_colour(
        args.light_colour, args.discover_colours, default_light_colour, "light_colour"
    )

    args.dark_colour = validate_replacement_colour(
        args.dark_colour, args.discover_colours, default_dark_colour, "dark_colour"
    )


def parse_colour(colour_str: str) -> tuple[int, int, int, int]:
    colour_values = colour_str.split(",")
    if len(colour_values) not in [3, 4]:
        raise argparse.ArgumentTypeError(
            "Colour must be specified as 3 or 4 "
            "comma-separated integers (RGB or RGBA)."
        )
    try:
        colour_ints = [int(val) for val in colour_values]
        if any(val < 0 or val > 255 for val in colour_ints):
            raise argparse.ArgumentTypeError(
                "Colour values must be in the range of 0-255."
            )
    except ValueError:
        raise argparse.ArgumentTypeError("Colour values must be integers.")

    if len(colour_ints) == 3:
        alpha: int = 255
    else:
        alpha: int = colour_ints[3]

    return colour_ints[0], colour_ints[1], colour_ints[2], alpha


__all__ = ["validate_args"]
