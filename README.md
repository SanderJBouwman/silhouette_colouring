# silhouette_colouring
This package is created to colour in silhouettes of gifs.

## Installation

Make sure git is installed on your system. If not, install it (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Run the following commands in your terminal to install the package:
```shell 
git clone https://github.com/SanderJBouwman/silhouette_colouring.git
cd silhouette_colouring
pip install .
```

## Issues 
### Terminal returns`command not found silhouette-col`
Try restaring terminal.  

### Images won't be coloured
The image expects the primary color to be the exact RGB value *(128, 128, 255)* or RGBA *(128, 128, 255, 255)*. The secondary color should be RGB *(0, 0, 255)* or RGBA *(0, 0, 255, 255)*.




## Usage
The package can be used to colour in silhouettes of images.
For more help run: 
```shell
silhouette-col -h
```

### Simple  
```shell
silhouette-col <path_to_csv> <path_to_images>
```

### Additional options 
Add output directory
```shell
silhouette-col <path_to_csv> <path_to_images> -o <path_to_output>
```

Change the darkening factor of the nucleus
```shell
silhouette-col <path_to_csv> <path_to_images> -d <darkening_factor>
```

## Author and maintainer
Sander J. Bouwman

