"""
This module contains the unit tests for the silhouette_colouring module.
"""

__author__ = "Sander J. Bouwman"

import unittest

import pandas as pd

from silhouette_colouring.src.utils import csv_is_valid, hex_to_rgb, \
    darken_color


class testColouring(unittest.TestCase):
    """
    Unit tests for the silhouette_colouring module which tests the following
    functions:
    - hex_to_rgb
    - darken_color
    - csv_is_valid
    """

    def test_hex_to_rgb(self) -> None:
        # Should be equal
        self.assertEqual((0, 0, 0), hex_to_rgb("#000000"))  # Pure black
        self.assertEqual((255, 255, 255), hex_to_rgb("#FFFFFF"))  # Pure white
        self.assertEqual((255, 0, 0), hex_to_rgb("#FF0000"))  # Pure red
        self.assertEqual((0, 255, 0), hex_to_rgb("#00FF00"))  # Pure green
        self.assertEqual((0, 0, 255), hex_to_rgb("#0000FF"))  # Pure blue

        # Should not be equal
        self.assertNotEqual(
            (0, 0, 0), hex_to_rgb("#FFFFFF")
        )  # Pure black vs pure white
        self.assertNotEqual(
            (255, 255, 255), hex_to_rgb("#000000")
        )  # Pure white vs pure black
        self.assertNotEqual(
            (255, 0, 0), hex_to_rgb("#00FF00")
        )  # Pure red vs pure green
        self.assertNotEqual(
            (0, 255, 0), hex_to_rgb("#0000FF")
        )  # Pure green vs pure blue

    def test_darken_color(self) -> None:
        darken_factor = 0.1
        red = (255, 0, 0)
        darkened_red = darken_color(red[0], red[1], red[2], darken_factor)
        self.assertLess(darkened_red[0], red[0])

        green = (0, 255, 0)
        darkened_green = darken_color(green[0], green[1], green[2], darken_factor)
        self.assertLess(darkened_green[1], green[1])

        # Light blue
        light_blue = (0, 255, 255)
        darkened_light_blue = darken_color(
            light_blue[0], light_blue[1], light_blue[2], darken_factor
        )
        self.assertLess(darkened_light_blue[1], light_blue[1])
        self.assertLess(darkened_light_blue[2], light_blue[2])

    def test_csv_validator(self) -> None:
        # Should be valid
        # Create a dataframe with the correct columns "cell_ID", "cluster", "color"
        valid_df = pd.DataFrame(
            {
                "cell_ID": [1, 2, 3],
                "cluster": [1, 2, 3],
                "color": ["#000000", "#FFFFFF", "#FF0000"],
            }
        )

        self.assertTrue(csv_is_valid(valid_df))

        # Should not be valid
        invalid_df = pd.DataFrame(
            {
                "cell_Isd": [1, 2, 3],
                "clustfer": [1, 2, 3],
                "colsour": ["#000000", "#FFFFFF", "#FF0000"],
            }
        )

        valid, missing_columns = csv_is_valid(invalid_df)
        self.assertFalse(valid)
        self.assertEqual(missing_columns, ["cell_ID", "cluster", "color"])


if __name__ == "__main__":
    unittest.main()
