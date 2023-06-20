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

## Issues 
### 1. Terminal returns`command not found silhouette-col`
Try restaring terminal.  

### 2. There is no difference between the input and ouput images. 
The input images are expected to have exact rgb values. These are locked and (currently) can't be changed.  

| Type      	| RGB value        	| RGBA value          	|
|-----------	|-----------------	|----------------------	|
| primary   	| (128, 128, 255) 	| (128, 128, 255, 255) 	|
| secondary 	| (0, 0, 255)     	| (0, 0, 255, 255)     	|

### 3. ImportError: No module named ...
Install the module using pip. For example: 
`pip install pandas`

## Parameters 
Required:  
| Parameter 	| Description                                                                                                                                                                          	| example            	| Default 	|
|-----------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------------	|---------	|
| arg 1     	| Path to a .csv file which will be used as reference for the colouring. It must have the following columns: 'cell_ID', 'cluster' and 'color'. The color should be given in HEX format 	| `../reference.csv` 	| None    	|
| arg 2     	| Path to directory that contains the GIF that will be used. (It will try to convert all GIF images in that directory so make sure only the right images are in it)                     	| `../gifs`          	| None    	|

Non-required:
| Parameter      	| Description                                                       	| example          	| Default       	|
|----------------	|-------------------------------------------------------------------	|------------------	|---------------	|
|`-o --output`    | Sets the output directory where the created images will be stored 	| `-o runs/output` 	| `working dir` 	|
|`-d --darkening` | Set the darkening factor. This value can be between 0.0 and 1.0   	| `-d 0.35`        	| `0.2`         	|

## Author and maintainer
Sander J. Bouwman

