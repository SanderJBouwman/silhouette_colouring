from setuptools import setup, find_packages

setup(
    name="silhouette_colouring",
    version="1.0",
    author="Sander J. Bouwman",
    description="Silhouette Colouring Tool",
    packages=find_packages(include=["silhouette_colouring", "silhouette_colouring.*"]),
    install_requires=[
        "pandas>=1.42.0",
        "Pillow>=9.5.0",
        "tqdm>=4.64.0",
        "numpy>=1.22.4",
    ],
    entry_points={
        "console_scripts": [
            "silhouette-col=silhouette_colouring.src.silhouette_colouring:main"
        ]
    },
)