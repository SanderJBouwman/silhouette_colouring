# silhouette_colouring
A simple commandline tool that allows the re-colouring of sillhouettes in large batches of GIF images.

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
The input images are expected to have exact rgb values. These are locked and (currently) can't be changed.  

| Type      	| RGB value        	| RGBA value          	|
|-----------	|-----------------	|----------------------	|
| primary   	| (128, 128, 255) 	| (128, 128, 255, 255) 	|
| secondary 	| (0, 0, 255)     	| (0, 0, 255, 255)     	|


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

