# silhouette_colouring
This package is created to colour in silhouettes of gifs.

## Requirements
`Pandas` and `Pillow` are required to run the package.

## Installation
Download the package and navigate to the directory. 
Run pip install -e . to install the package.

## Usage
The package can be used to colour in silhouettes of images.
For more help run ```shell silhouette_colouring -h```

### Simple  
```shell
silhouette_colouring <path_to_csv> <path_to_images>
```

### Additional options 
Add output directory
```shell
silhouette_colouring <path_to_csv> <path_to_images> -o <path_to_output>
```

Change the darkening factor of the nucleus
```shell
silhouette_colouring <path_to_csv> <path_to_images> -d <darkening_factor>
```

## Author and maintainer
Sander J. Bouwman

