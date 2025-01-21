"""Pyramid Generator 2D."""
import logging
import pathlib
import typing

from argolid import PyramidGenerartor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def pyramid_generator_2d_single_img(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    min_dim: int,
    output_format: str,
    downsample_dict: typing.Dict[int, str],
):
    """Pyramid Generator 2D.

    Args:
        input_path (pathlib.Path): Path to the input image.
        output_path (pathlib.Path): Path to the output directory.
        min_dim (int): Minimum dimension of the image pyramid.
        output_format (str): Output image format.
        downsample_dict (typing.Dict[int, str]): Dictionary with channel number as key and method as value.
    """
    pg = PyramidGenerartor()
    logger.info("Downsample method: %s", downsample_dict)
    pg.generate_from_single_image(
        input_file=input_path,
        output_dir=output_path,
        min_dim=min_dim,
        vis_type=output_format,
        ds_dict=downsample_dict,
    )


def pyramid_generator_2d_img_collection(
    input_path: pathlib.Path,
    filename_pattern: str,
    out_img_name: str,
    output_path: pathlib.Path,
    min_dim: int,
    output_format: str,
    downsample_dict: typing.Dict[int, str],
):
    """Pyramid Generator 2D.

    Args:
        input_path (pathlib.Path): Path to the input directory.
        filename_pattern (str): Filename pattern.
        output_path (pathlib.Path): Path to the output directory.
        out_img_name (str): Name of the output image.
        min_dim (int): Minimum dimension of the image pyramid.
        output_format (str): Output image format.
        downsample_dict (typing.Dict[int, str]): Dictionary with channel number as key and method as value.
    """
    pg = PyramidGenerartor()
    pg.generate_from_image_collection(
        collection_path=input_path,
        pattern=filename_pattern,
        image_name=out_img_name,
        output_dir=output_path,
        min_dim=min_dim,
        vis_type=output_format,
        ds_dict=downsample_dict,
    )
