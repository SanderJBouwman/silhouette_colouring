[![Lint](https://github.com/SanderJBouwman/silhouette_colouring/actions/workflows/black.yml/badge.svg)](https://github.com/SanderJBouwman/silhouette_colouring/actions/workflows/black.yml)
# silhouette_colouring

A simple command-line tool that allows the recoloring of silhouettes in large batches of GIF images.

---

## Installation

>**Note**: Make sure Git is installed on your system. If not, install it from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

There are two options for installation:

### Option 1: Installing directly from GitHub

```shell
pip install 'silhouette_colouring @ git+https://github.com/SanderJBouwman/silhouette_colouring.git'
```

### Option 2: Cloning the repository and then installing

```shell 
git clone https://github.com/SanderJBouwman/silhouette_colouring.git
cd silhouette_colouring
pip install .
```

---

## Usage

>**Note**: If your terminal returns `command not found silhouette-col` after installation, restarting your terminal will most likely fix this issue.

The package can be used to color in silhouettes of images. For more help, run:

```shell
silhouette-col -h
```

### Simple usage

```shell
silhouette-col <path_to_csv> <path_to_images>
```

### Additional options 

Add an output directory:

```shell
silhouette-col <path_to_csv> <path_to_images> -o <path_to_output>
```

Change the darkening factor of the nucleus:

```shell
silhouette-col <path_to_csv> <path_to_images> -d <darkening_factor>
```

Use discovery mode, which is useful if the light and dark colors of the image are unknown or not constant:

```shell
silhouette-col <path_to_csv> <path_to_images> --discover-colours
```

Set the light color and dark color to non-standard values:

```shell
silhouette-col <path_to_csv> <path_to_images> --light-colour 255,255,255 --dark-colour 128,255,255
```

---

## Issues 

### 1. Terminal returns `command not found silhouette-col`

- Try restarting the terminal.

### 2. There is no difference between the input and output images.

- Supply the `--verbose` flag, which will print all received errors to the console. This makes it easier to find the issue.

- The input images are colored using the received colors from the `--light-colour` and `--dark-colour` arguments. If they are not supplied, the default values are used (see table below).

| Type      	| RGB value        	| RGBA value          	|
|-----------	|-----------------	|----------------------	|
| primary (light)   	| (128, 128, 255) 	| (128, 128, 255, 255) 	|
| secondary (dark) 	| (0, 0, 255)     	| (0, 0, 255, 255)     	|

>**Note**: If you don't want to set the colors directly, you can use the `--discover-colours` parameter, which will attempt to find the primary and secondary colors by itself.

### 3. ImportError: No module named ...

- Install the missing module using pip. For example: 
  `pip install pandas`

---

## Parameters 
**Required**:

| Parameter   | Description                                                                                                                                                                                                                         | Example             | Default |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|---------|
| arg 1       | Path to a .csv file which will be used as a reference for the coloring. It must have the following columns: 'cell_ID', 'cluster', and 'color'. The color should be given in HEX format.                                              | `../reference.csv`  | None    |
| arg 2       | Path to the directory that contains the GIFs to be used. It will try to convert all GIF images in that directory, so make sure only the right images are in it.                                                                    | `../gifs`           | None    |

**Non-required**:

| Long option | Short option | Description | Example | Default |
|---|---|---|---|---|
| `--output` | `-o` | Sets the output directory where the created images will be stored | `-o runs/output` | `working dir` |
| `--darkening` | `-d` | Set the darkening factor. This value can be between 0.0 and 1.0 | `-d 0.35` | `0.2` |
| `--dark-colour` | None | Specify the RGB or RGBA colors of the dark color | `--dark-colour 0,0,255,255` | `0,0,255` |
| `--light-colour` | None | Specify the RGB or RGBA colors of the light color | `--light-colour 128,128,255,255` | `128,128,255` |
| `--discover-colours` | None | Analyze every image and assign the second and third most common colors to `--light-colour` and `--dark-colour` | `--discover-colours` | False |
| `--verbose` | `-v` | Run the script in verbose mode, which will print more information to the screen | `--verbose` | False |

## Author and Maintainer
Sander J. Bouwman
