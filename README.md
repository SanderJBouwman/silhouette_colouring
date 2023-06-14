# silhouette_colouring
This package is created to colour in silhouettes of gifs.

## Requirements
`Pandas` and `Pillow` are required to run the package.

## Installation

Make sure git is installed on your system. If not, install it (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Run the following commands in your terminal to install the package:
```shell 
git clone git@github.com:SanderJBouwman/silhouette_colouring.git
cd silhouette_colouring
pip install -e -u .
```

## Usage
The package can be used to colour in silhouettes of images.
For more help run: 
```shell
silhouette_colouring -h
```

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

