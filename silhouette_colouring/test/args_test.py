import unittest
import argparse
from pathlib import Path
from unittest.mock import patch

from silhouette_colouring.src.silhouette_colouring import parse_arguments


class MyTestCase(unittest.TestCase):

    def test_all_okay(self):
        # Print current working directory
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--outputDir', 'test_files/test_output'
        ]):
            try:
                args = parse_arguments()
            except Exception as e:
                self.fail(f"Exception raised: {e}")

    def test_wrong_csv_path(self):
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv_wrong.csv',
            'test_files/test_images',
            '--darkening', '0.2',
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                args = parse_arguments()

    def test_wrong_gif_input_dir(self):
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images_wrong',
            '--darkening', '0.2',
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                args = parse_arguments()

    def test_wrong_darkening_factor(self):
        with patch('argparse._sys.argv', [
            'test_script.py',
            'test_files/test_csv.csv',
            'test_files/test_images',
            '--darkening', '-1',
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(ValueError):
                args = parse_arguments()


if __name__ == '__main__':
    unittest.main()
