import argparse
import unittest
from pathlib import Path

from silhouette_colouring.src.validators import (
    validate_input_csv,
    validate_gif_input_dir,
    validate_output_dir,
    validate_darkening_factor,
    validate_input_colour,
    validate_replacement_colour,
    parse_colour,
)


class TestScript(unittest.TestCase):
    def test_validate_input_csv_exists(self):
        input_csv = Path("silhouette_colouring/test/test_files/test_csv.csv")
        self.assertIsNone(validate_input_csv(input_csv))

    def test_validate_input_csv_not_exists(self):
        input_csv = Path("nonexistent/file.csv")
        with self.assertRaises(FileNotFoundError):
            validate_input_csv(input_csv)

    def test_validate_input_csv_not_csv_file(self):
        input_csv = Path("silhouette_colouring/test/test_files/faulty_filetype.txt")
        with self.assertRaises(ValueError):
            validate_input_csv(input_csv)

    def test_validate_gif_input_dir_exists(self):
        gif_input_dir = Path("silhouette_colouring/test/test_files/test_images")
        self.assertIsNone(validate_gif_input_dir(gif_input_dir))

    def test_validate_gif_input_dir_not_exists(self):
        gif_input_dir = Path(
            "silhouette_colouring/test/test_files" "/some_nonexistent_dir"
        )
        with self.assertRaises(FileNotFoundError):
            validate_gif_input_dir(gif_input_dir)

    def test_validate_gif_input_dir_not_directory(self):
        gif_input_dir = Path(
            "silhouette_colouring/test" "/test_files/test_images/file.gif"
        )
        with self.assertRaises(ValueError):
            validate_gif_input_dir(gif_input_dir)

    def test_validate_gif_input_dir_no_gifs(self):
        gif_input_dir = Path("silhouette_colouring/test/test_files/empty_dir")
        with self.assertRaises(ValueError):
            validate_gif_input_dir(gif_input_dir)

    def test_validate_output_dir_exists(self):
        output_dir = Path(
            "silhouette_colouring/test/test_files" "/test_images/SilhouetteOutput"
        )
        self.assertIsNone(validate_output_dir(output_dir))

    def test_validate_output_dir_not_exists(self):
        output_dir = Path(
            "silhouette_colouring/test/test_files" "/some_nonexistent_dir"
        )
        with self.assertRaises(FileNotFoundError):
            validate_output_dir(output_dir)

    def test_validate_output_dir_not_directory(self):
        output_dir = Path(
            "silhouette_colouring/test" "/test_files/test_images/file.gif"
        )
        with self.assertRaises(ValueError):
            validate_output_dir(output_dir)

    def test_validate_darkening_factor_valid(self):
        darkening_factors = [0.5, 0.75, 1.0, 1, 0]
        for darkening_factor in darkening_factors:
            with self.subTest(darkening_factor=darkening_factor):
                self.assertIsNone(validate_darkening_factor(darkening_factor))

    def test_validate_darkening_factor_invalid(self):
        darkening_factors = [
            [-1, ValueError],
            [1.1, ValueError],
            ["string", TypeError],
            [None, TypeError],
        ]

        for darkening_factor in darkening_factors:
            with self.subTest(darkening_factor=darkening_factor):
                with self.assertRaises(darkening_factor[1]):
                    validate_darkening_factor(darkening_factor[0])

    def test_validate_input_colour_valid(self):
        valid_colours = [
            "255,255,255,255",
            "0,0,0,0",
            "128,128,128,128",
            "255,0,0",
            None,
        ]
        for colour in valid_colours:
            with self.subTest(colour=colour):
                self.assertIsNone(validate_input_colour(colour))

    def test_validate_input_colour_invalid(self):
        invalid_colours = [
            "255,255,255,255,255",
            "0,0,0,0,0",
            "128,128,-10" "255,280,0",
            "256,0,0",
        ]

        for colour in invalid_colours:
            with self.subTest(colour=colour):
                with self.assertRaises(argparse.ArgumentTypeError):
                    validate_input_colour(colour)

        invalid_types = [[255, TypeError], [True, TypeError]]

        for colour in invalid_types:
            with self.subTest(colour=colour):
                with self.assertRaises(colour[1]):
                    validate_input_colour(colour[0])

    def test_validate_replacement_colour_discover_colours(self):
        replacement_colour = None
        discover_colours = True
        default_color = "128,128,255,255"
        argument_name = "light_colour"
        result = validate_replacement_colour(
            replacement_colour, discover_colours, default_color, argument_name
        )
        self.assertIsNone(result)

    def test_validate_replacement_colour_not_discover_colours(self):
        replacement_colour = "255,255,255,255"
        discover_colours = False
        default_color = "128,128,255,255"
        argument_name = "light_colour"
        result = validate_replacement_colour(
            replacement_colour, discover_colours, default_color, argument_name
        )
        expected_result = parse_colour(replacement_colour)
        self.assertEqual(result, expected_result)

    def test_validate_replacement_colour_not_discover_colours_no_value(self):
        replacement_colour = None
        discover_colours = False
        default_color = "128,128,255,255"
        argument_name = "light_colour"
        result = validate_replacement_colour(
            replacement_colour, discover_colours, default_color, argument_name
        )
        expected_result = parse_colour(default_color)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
