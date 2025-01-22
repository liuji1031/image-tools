# Pyramid Generator 2D (0.1.1-dev0)

This image tool generates 2D image pyramid from either a single image or a directory of images (with stitching vector). This tool is a wrapper for the 2D pyramid generator functionalities implemented in Argolid.

## Options
| Name        | Description                                                                 | I/O | Type   | Required |
|-------------|-----------------------------------------------------------------------------|-----|--------| ---------|
| `--inputPath`        | Path to directory containing images or path to a single image.              | Input   | collection | Yes |
| `--filePattern`  | Filename pattern used to select images from input directory. <br/>Ignored if input is a single image.  | Input   | string | No, unless `--inputPath` is a directory |
| `--outputPath`       | Path of output directory.                                                 | Output   | collection    | Yes |
| `--outImgName`       | Name of the output image. Only needed when input is a directory.         | Input   | string    | No, unless `--inputPath` is a directory |
| `--minDim`           | Minimum dimension of the image pyramid.                            | Input   | integer | Yes |
| `--outputFormat`     | Output format of the image pyramid. Options are "NG_Zarr", "PCNG", "Viv".  | Input   | string | Yes |
| `--downsampleMethod` | Downsample method. Specify using a dictionary string with the <br/> channel number as the key and the method as the value. channel <br/>number ranges from 0 to n_channels-1. Available methods are <br/>"mean", "mode_max", "mode_min". Example: '{0:\"mean\"}'. <br/>If not specified, all channels will be downsampled using "mean". | Input   | string    | No |

## Usage
### Single image
For processing a single image, the required options are: `--inputPath`, `--outputPath`, `--minDim`, `--outputFormat`
Example command line usage with Python:
```
python3 -m polus.images.formats.pyramid-generator-2d --inputPath /path/to/single/image.tiff --outputPath /path/to/output --minDim 1024 --outputFormat NG_Zarr --downsampleMethod '{0:"mean"}'
```

### Image collection
For processing a image collection, the required options are `--inputPath`,`--filePattern`, `--outputPath`,`outImgName`, `--minDim`, `--outputFormat`
Example command line usage with Python:
```
python3 -m polus.images.formats.pyramid-generator-2d --inputPath /path/to/image_collection --filePattern 'img_x{x:d}_y{y:d}_c{c:d}.ome.tiff' --outputPath /path/to/output --outImgName output_image --minDim 1024 --outputFormat NG_Zarr --downsampleMethod '{0:"mean"}'
```

## Building

To build the Docker image for the tool, run `./build-docker.sh`.

## Install WIPP Plugin

If WIPP is running, navigate to the plugins page and add a new plugin. Paste the
contents of `plugin.json` into the pop-up window and submit.
