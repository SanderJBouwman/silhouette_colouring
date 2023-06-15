from setuptools import setup, find_packages

setup(
    name="silhouette_colouring",
    version="1.0",
    author="Sander J. Bouwman",
    description="Silhouette Colouring Tool",
    packages=find_packages(include=["silhouette_colouring", "silhouette_colouring.*"]),
    extras_require={
        "pandas": "",
        "Pillow": "",
        "tqdm": "",
    },
    entry_points={
        "console_scripts": [
            "silhouette-col=silhouette_colouring.src.silhouette_colouring:main"
        ]
    },
)