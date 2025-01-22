"""Pyramid Generator 2D."""
import logging
import pathlib
import typing
from enum import Enum

from argolid import PyramidGenerartor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OutputFormat(str, Enum):
    """Available output formats."""

    NG_Zarr = "NG_Zarr"
    PCNG = "PCNG"
    Viv = "Viv"


def pyramid_generator_2d_single_img(
    inp_dir: pathlib.Path,
    out_dir: pathlib.Path,
    min_dim: int,
    out_format: str,
    ds_dict: typing.Dict[int, str],
):
    """Pyramid Generator 2D.

    Args:
        inp_dir (pathlib.Path): Path to the input image.
        out_dir (pathlib.Path): Path to the output directory.
        min_dim (int): Minimum dimension of the image pyramid.
        out_format (str): Output image format.
        ds_dict (typing.Dict[int, str]): Dictionary with channel number as key and method as value.
    """
    pg = PyramidGenerartor()
    logger.info("Downsample method: %s", ds_dict)
    pg.generate_from_single_image(
        input_file=inp_dir,
        output_dir=out_dir,
        min_dim=min_dim,
        vis_type=out_format,
        ds_dict=ds_dict,
    )


def pyramid_generator_2d_img_collection(
    inp_dir: pathlib.Path,
    file_pattern: str,
    out_img_name: str,
    out_dir: pathlib.Path,
    min_dim: int,
    out_format: str,
    ds_dict: typing.Dict[int, str],
):
    """Pyramid Generator 2D.

    Args:
        inp_dir (pathlib.Path): Path to the input directory.
        file_pattern (str): Filename pattern.
        out_dir (pathlib.Path): Path to the output directory.
        out_img_name (str): Name of the output image.
        min_dim (int): Minimum dimension of the image pyramid.
        out_format (str): Output image format.
        ds_dict (typing.Dict[int, str]): Dictionary with channel number as key and method as value.
    """
    pg = PyramidGenerartor()
    pg.generate_from_image_collection(
        collection_path=inp_dir,
        pattern=file_pattern,
        image_name=out_img_name,
        output_dir=out_dir,
        min_dim=min_dim,
        vis_type=out_format,
        ds_dict=ds_dict,
    )
