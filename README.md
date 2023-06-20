# silhouette_colouring
A simple commandline tool that allows the re-colouring of sillhouettes in large batches of GIF images.

## Installation
>Note: Make sure git is installed on your system. If not, install it (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  


There are two options of installation: 
### Option 1: Installing directly from GitHub:
>```shell
>pip install 'silhouette_colouring @ git+https://github.com/SanderJBouwman/silhouette_colouring.git'
>```

### Option 2: Cloning the repository then installing: 
>```shell 
>git clone https://github.com/SanderJBouwman/silhouette_colouring.git
>cd silhouette_colouring
>pip install .
>```

## Usage
>*Note: It might be possible that your terminal returns `command not found silhouette-col` after installation. Restarting your terminal will most possibly fix this issue.*  

The package can be used to colour in silhouettes of images.
For more help run: 
>```shell
>silhouette-col -h
>```

### Simple  
>```shell
>silhouette-col <path_to_csv> <path_to_images>
>```

### Additional options 
Add output directory
>```shell
>silhouette-col <path_to_csv> <path_to_images> -o <path_to_output>
>```

Change the darkening factor of the nucleus
>```shell
>silhouette-col <path_to_csv> <path_to_images> -d <darkening_factor>
>```

Using discovery mode, which is usefull if the light and dark colours of the image unknown or are not constant  
>```shell
>silhouette-col <path_to_csv> <path_to_images> --discover-colours
>```

Setting the light colour and dark colour to non-standard
>```shell
>silhouette-col <path_to_csv> <path_to_images> --light-colour 255,255,255 --dark-colour 128,255,255
>```

## Issues 
### 1. Terminal returns`command not found silhouette-col`
* Try restaring terminal.  

### 2. There is no difference between the input and ouput images. 
* Supply the `--verbose' flag, which will print all received errors to the console. This makes it easier to find the issue.  

* The input images are coloured using the received colours from the `--light-colour` and `--dark-colour` arguments. If they are not supplied the default values are used (see table below).

| Type      	| RGB value        	| RGBA value          	|
|-----------	|-----------------	|----------------------	|
| primary (light)   	| (128, 128, 255) 	| (128, 128, 255, 255) 	|
| secondary (dark) 	| (0, 0, 255)     	| (0, 0, 255, 255)     	|

>*Note: If you don't want to set the colours directly, you can parse the `--discover-colours` parameter which will attempt to find the primary and secondary colours by itself.*


### 3. ImportError: No module named ...
* Install the module using pip. For example: 
`pip install pandas`

## Parameters 
Required:  
| Parameter 	| Description                                                                                                                                                                          	| example            	| Default 	|
|-----------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------------	|---------	|
| arg 1     	| Path to a .csv file which will be used as reference for the colouring. It must have the following columns: 'cell_ID', 'cluster' and 'color'. The color should be given in HEX format 	| `../reference.csv` 	| None    	|
| arg 2     	| Path to directory that contains the GIF that will be used. (It will try to convert all GIF images in that directory so make sure only the right images are in it)                     	| `../gifs`          	| None    	|

Non-required:
| Long option | Short option | Description | example | Default |
|---|---|---|---|---|
| `--output` | `-o` | Sets the output directory where the created images will be stored | `-o runs/output` | `working dir` |
| `--darkening` | `-d` | Set the darkening factor. This value can be between 0.0 and 1.0 | `-d 0.35` | `0.2` |
| `--dark-colour` | None | Specify the RGB or RGBA colours of the dark colour | `--dark-colour 0,0,255,255` | `0,0,255` |
| `--light-colour` | None | Specify the RGB or RGBA colours of the light colour | `--light-colour 128,128,255,255` | `128,128,255` |
| `--discover-colours` | None | Every image will get analysed. The second and third most common colours will be assigned to --light-colour and --dark-colour. | `--discover-colours` | False |
| `--verbose` | `-v` | Run the script in verbose mode, which will print more information to screen. | `--verbose` | False |
## Author and maintainer
Sander J. Bouwman

