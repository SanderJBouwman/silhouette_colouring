import unittest
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
                parse_arguments()
            except Exception as error:
                self.fail(f"Exception raised: {error}")

    def test_wrong_csv_path(self):
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
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                parse_arguments()

    def test_wrong_gif_input_dir(self):
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
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(FileNotFoundError):
                parse_arguments()

    def test_wrong_darkening_factor(self):
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
            '--outputDir', 'test_files/test_output'
        ]):
            with self.assertRaises(ValueError):
                parse_arguments()


if __name__ == '__main__':
    unittest.main()
