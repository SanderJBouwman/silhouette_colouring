import argparse
import unittest
from unittest.mock import patch

from silhouette_colouring.src.silhouette_colouring import parse_arguments


class MyTestCase(unittest.TestCase):

    def test_all_okay(self) -> None:
        # Print current working directory
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/test_output'
        ]):
            try:
                parse_arguments()
            except Exception as error:
                self.fail(f"Exception raised: {error}")

    def test_wrong_csv_path(self) -> None:
        """
        Test if FileNotFoundError is raised when the CSV path is wrong
        (does not exist)
        :return: None
        """
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv_wrong.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                parse_arguments()

    def test_wrong_gif_input_dir(self) -> None:
        """
        Test if FileNotFoundError is raised when the GIF
        input directory is wrong (does not exist)
        :return: None
        """
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images_wrong',
            '--darkening', '0.2',
            '--output', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                parse_arguments()

    def test_wrong_output_dir(self) -> None:
        """
        Test if FileNotFoundError is raised when the output directory is wrong
        (does not exist)
        :return: None
        """
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/a_not_existing_dir'
        ]):
            with self.assertRaises(FileNotFoundError):
                parse_arguments()

    def test_wrong_darkening_factor(self) -> None:
        """
        Test if ValueError is raised when the darkening factor is wrong
        (not between 0 and 1)
        :return: None
        """
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '-1',
            '--output', 'test_files/test_output'
        ]):
            with self.assertRaises(ValueError):
                parse_arguments()

    def test_colour_okay(self) -> None:
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/test_output',
            '--dark-colour', '0,0,255',
            '--light-colour', '128,128,255,255'
        ]):
            try:
                parse_arguments()
            except Exception as error:
                self.fail(f"Exception raised: {error}")

    def test_wrong_dark_colour(self) -> None:
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/test_output',
            '--dark-colour', '0,0',
            '--light-colour', '128,128,255'
        ]):
            with self.assertRaises(argparse.ArgumentTypeError):
                parse_arguments()

    def test_wrong_light_colour(self) -> None:
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--output', 'test_files/test_output',
            '--dark-colour', '0,0,255',
            '--light-colour', '128,128'
        ]):
            with self.assertRaises(argparse.ArgumentTypeError):
                parse_arguments()

if __name__ == '__main__':
    unittest.main()
