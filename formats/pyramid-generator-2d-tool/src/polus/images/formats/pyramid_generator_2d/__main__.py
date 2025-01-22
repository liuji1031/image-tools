"""CLI for the Pyramid Generator 2D tool."""

import logging
import os
import pathlib
from ast import literal_eval

import typer
from polus.images.formats.pyramid_generator_2d.pyramid_generator_2d import (
    pyramid_generator_2d_img_collection,
    pyramid_generator_2d_single_img,
)

logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
POLUS_LOG = getattr(logging, os.environ.get("POLUS_LOG", "INFO"))
logger = logging.getLogger("polus.images.formats.pyramid_generator_2d")
logger.setLevel(POLUS_LOG)

app = typer.Typer()


def _validate_params(
    input_path: pathlib.Path,
    file_pattern: str,
    out_img_name: str,
    output_format: str,
    downsample_method: str,
):
    """Validate the command line parameters.

    Args:
        input_path (pathlib.Path): input path to single image or directory
        file_pattern (str): filename pattern used to select images from input directory
        out_img_name (str): name of the output image
        output_format (str): output format of the image pyramid
        downsample_method (str): downsample method

    Returns:
        bool: True if generating from single image, False if generating from image collection
        dict: parsed downsample method
    """
    gen_from_single_img = False
    if input_path.is_dir():
        logger.info("Input is a directory.")
        # Generate pyramid from image collection
        if file_pattern == "":
            raise ValueError(
                "Filename pattern must be provided when input is a directory."
            )
        if out_img_name == "":
            raise ValueError(
                "Output image name must be provided when input is a directory."
            )
    elif input_path.is_file():
        logger.info("Input is a single image.")
        # Generate pyramid from single image
        gen_from_single_img = True

    # parse downsample method, turn string into dictionary
    downsample_dict = {}
    if downsample_method:
        try:
            downsample_dict = literal_eval(downsample_method)
        except Exception as e:
            raise ValueError("Invalid downsample method.") from e

    # validate output format
    available_formats = {"NG_Zarr", "PCNG", "Viv"}
    if output_format not in available_formats:
        raise ValueError("Invalid output format.")

    # validate downsample method
    avaliable_methods = {"mean", "mode_max", "mode_min"}
    for _, value in downsample_dict.items():
        if value not in avaliable_methods:
            raise ValueError("Invalid downsample method.")

    return gen_from_single_img, downsample_dict


@app.command()
def main(
    input_path: pathlib.Path = typer.Option(
        ...,
        "--inputPath",
        help="Path to directory containing images or path to a single image.",
        exists=True,
        readable=True,
        resolve_path=True,
        file_okay=True,
        dir_okay=True,
    ),
    file_pattern: str = typer.Option(
        "",
        "--filePattern",
        help=(
            "Filename pattern used to select images from input directory. "
            "Ignored if input is a single image."
        ),
    ),
    output_path: pathlib.Path = typer.Option(
        ...,
        "--outputPath",
        help="Path of output directory.",
        exists=True,
        writable=True,
        resolve_path=True,
        file_okay=False,
    ),
    out_img_name: str = typer.Option(
        "",
        "--outImgName",
        help="Name of the output image. Only needed when input is a directory.",
    ),
    min_dim: int = typer.Option(
        ...,
        "--minDim",
        help="Minimum dimension of the image pyramid.",
    ),
    output_format: str = typer.Option(
        ...,
        "--outputFormat",
        help="Output format of the image pyramid. Options are 'NG_Zarr', 'PCNG', 'Viv'.",
    ),
    downsample_method: str = typer.Option(
        "",
        "--downsampleMethod",
        help=(
            "Downsample method. Specify using a dictionary string with the "
            "channel number as the key and the method as the value. channel "
            "number ranges from 0 to n_channels - 1. available methods are "
            "'mean', 'mode_max', 'mode_min'. Example: '{0:\"mean\", 1:\"mode_max\"}'. "
            "If not specified, all channels will be downsampled using the mean "
        ),
    ),
) -> None:
    """CLI for the Pyramid Generator tool.

    Calls the Pyramid Generator tool to generate image pyramids from a single image or a collection of images.

    Args:
        input_path (pathlib.Path): Path to directory containing images or path to a single image.
        file_pattern (str): Filename pattern used to select images from input directory. Ignored if input is a single image.
        output_path (pathlib.Path): Path to output directory.
        out_img_name (str): Name of the output image. Only needed when input is a directory.
        min_dim (int): Minimum dimension of the image pyramid.
        output_format (str): Output format of the image pyramid. Options are 'NG_Zarr', 'PCNG', 'Viv'.
        downsample_method (str): Downsample method. Specify using a dictionary string with the channel number as the key and the method as the value. channel number ranges from 0 to n_channels - 1. available methods are 'mean', 'mode_max', 'mode_min'. Example: '{0:mean, 1:mode_max}'If not specified, all channels will be downsampled using the mean
    """
    logger.info("Starting Pyramid Generator Tool ...")

    logger.info("inputPath = %s", str(input_path))
    logger.info("filePattern = %s", file_pattern if file_pattern else "N/A")
    logger.info("outputPath = %s", output_path)
    logger.info("outImgName = %s", out_img_name if out_img_name else "N/A")
    logger.info("minDim = %d", min_dim)
    logger.info("outputFormat = %s", output_format)
    logger.info("downsampleMethod = %s", downsample_method)

    gen_from_single_img, downsample_dict = _validate_params(
        input_path=input_path,
        file_pattern=file_pattern,
        out_img_name=out_img_name,
        output_format=output_format,
        downsample_method=downsample_method,
    )

    # call argolid
    if gen_from_single_img:
        pyramid_generator_2d_single_img(
            input_path=str(input_path),
            output_path=str(output_path),
            min_dim=min_dim,
            output_format=output_format,
            downsample_dict=downsample_dict,
        )
    else:
        pyramid_generator_2d_img_collection(
            input_path=str(input_path),
            file_pattern=file_pattern,
            out_img_name=out_img_name,
            output_path=str(output_path),
            min_dim=min_dim,
            output_format=output_format,
            downsample_dict=downsample_dict,
        )


if __name__ == "__main__":
    app()
