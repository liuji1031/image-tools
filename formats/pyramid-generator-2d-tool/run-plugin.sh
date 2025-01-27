#!/bin/bash

version=$(<VERSION)

container_input_dir="/inpDir"
container_output_dir="/outDir"

################ example usage 1, single image ################

# Update with your data
inpDir=/tmp/path/to/single/image.tif
outDir=/tmp/path/to/output
minDim=128
outFormat="NG_Zarr"
dsMethod="{0:"mean"}"

docker run -v $inpDir:/${container_input_dir} \
           -v $outDir:/${container_output_dir} \
            --user $(id -u):$(id -g) \
            polusai/pyramid-generator-2d-tool:${version} \
            --inpDir ${container_input_dir} \
            --outDir ${container_output_dir} \
            --minDim ${minDim} \
            --outFormat ${outFormat} \
            --dsMethod ${dsMethod}

############# example usage 2, image collection ###############

inpDir=/tmp/path/to/input
filepattern="pattern"
outDir=/tmp/path/to/output
outImgName="output_image"
minDim=128
outFormat="NG_Zarr"
dsMethod="{0:"mean"}"

docker run -v $inpDir:/${container_input_dir} \
           -v $outDir:/${container_output_dir} \
            --user $(id -u):$(id -g) \
            polusai/pyramid-generator-2d-tool:${version} \
            --inpDir ${container_input_dir} \
            --filepattern ${filepattern} \
            --outDir ${container_output_dir} \
            --outImgName ${outImgName} \
            --minDim ${minDim} \
            --outFormat ${outFormat} \
            --dsMethod ${dsMethod}
