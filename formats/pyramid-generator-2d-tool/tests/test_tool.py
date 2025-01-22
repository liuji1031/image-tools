"""Testing the Command Line Tool."""

import faulthandler
import logging
import shutil
import typing
from pathlib import Path

import bfio
import numpy as np
import pytest
import requests
from polus.images.formats.pyramid_generator_2d.__main__ import _validate_params, app
from typer.testing import CliRunner

faulthandler.enable()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _get_real_img(path2save: Path, filename=None) -> Path:
    """Download a real image from the internet.

    Args:
        path2save (Path): path to save the image

    Returns:
        Path : path to the downloaded image
    """
    # Download the data if it doesn't exist
    URL = "https://github.com/usnistgov/WIPP/raw/master/data/PyramidBuilding/inputCollection/"
    filename = "img_r001_c001.ome.tif" if filename is None else filename
    if not (path2save / filename).exists():
        content = requests.get(URL + filename, timeout=10.0).content
        (path2save / filename).open("wb").write(content)

    return path2save / filename


def _gen_random_img(path2save: Path, filename: str, size: int):
    """Generate a random image.

    Args:
        path2save (Path): path to save the image
        filename (str): name of the file
        size (int): size of the image
    Returns:
        str : path to the generated image
    """
    # Generate a random image
    with bfio.BioWriter(path2save / filename) as bw:
        bw.X = size
        bw.Y = size
        bw.dtype = np.uint8
        bw[:] = np.random.randint(
            np.iinfo(bw.dtype).min, np.iinfo(bw.dtype).max, (bw.X, bw.Y), dtype=bw.dtype
        )

    return str(path2save / filename)


@pytest.fixture
def gen_single_image_path() -> typing.Generator[typing.Tuple[Path, Path], None, None]:
    """Generate input and output path for single image test."""
    input_path = Path("data/input/single_image")
    input_path.mkdir(parents=True, exist_ok=True)

    output_path = Path("data/output/single_image")
    output_path.mkdir(parents=True, exist_ok=True)

    yield input_path, output_path

    # delete the input and output path
    shutil.rmtree(input_path)
    shutil.rmtree(output_path)


@pytest.fixture
def gen_single_image(
    gen_single_image_path,
) -> typing.Generator[typing.Tuple[Path, Path], None, None]:
    """Create a single image."""
    input_path, output_path = gen_single_image_path

    # img_path = _gen_random_img(input_path, "random_img.tif", 2048)
    img_path = _get_real_img(input_path)

    yield img_path, output_path

    # delete the image
    img_path.unlink()


@pytest.fixture
def gen_image_collection_path() -> (
    typing.Generator[typing.Tuple[Path, Path], None, None]
):
    """Generate input and output path for image collection test."""
    input_path = Path("data/input/image_collection")
    input_path.mkdir(parents=True, exist_ok=True)

    output_path = Path("data/output/image_collection")
    output_path.mkdir(parents=True, exist_ok=True)

    yield input_path, output_path

    # delete the input and output path
    shutil.rmtree(input_path)
    shutil.rmtree(output_path)


@pytest.fixture
def gen_image_collection(
    gen_image_collection_path,
) -> typing.Generator[typing.Tuple[Path, Path, str, str], None, None]:
    """Create an image collection."""
    input_path, output_path = gen_image_collection_path

    img_paths = []
    for i in range(3):
        img_path = _get_real_img(input_path, f"img_r001_c{i:03d}.ome.tif")
        img_paths.append(img_path)

    file_pattern = "img_r001_c{c:d}.ome.tif"
    out_img_name = "output_img"
    yield input_path, output_path, file_pattern, out_img_name

    # delete the image
    for img_path in img_paths:
        img_path.unlink()


@pytest.fixture(
    params=[[128, "NG_Zarr", '{0: "mean"}'], [128, "Viv", '{0: "mean"}']],
    ids=["128_NG_Zarr", "128_Viv"],
)
def gen_process_params(request):
    """Return the default parameters for the single image."""
    return request.param


def test_cli_single_img(gen_single_image, gen_process_params):
    """Test the command line."""
    input_path, output_path = gen_single_image
    min_dim, output_format, downsample_dict = gen_process_params

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inputPath",
            str(input_path),
            "--outputPath",
            str(output_path),
            "--minDim",
            min_dim,
            "--outputFormat",
            output_format,
            "--downsampleMethod",
            downsample_dict,
        ],
    )

    # Test for a successful run
    assert result.exit_code == 0


@pytest.mark.skip(reason="Image collection set seems to need stitching vector")
def test_cli_image_collection(gen_image_collection, gen_process_params):
    """Test the command line."""
    input_path, output_path, file_pattern, out_img_name = gen_image_collection
    min_dim, output_format, downsample_dict = gen_process_params
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inputPath",
            str(input_path),
            "--outputPath",
            str(output_path),
            "--filenamePattern",
            file_pattern,
            "--outImgName",
            out_img_name,
            "--minDim",
            min_dim,
            "--outputFormat",
            output_format,
            "--downsampleMethod",
            downsample_dict,
        ],
    )

    # Test for a successful run
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "filename_pattern,out_img_name,output_format,downsample_method",
    [
        ("", "output_image", "NG_Zarr", ""),  # empty filename pattern
        ("img_r{r:d}_c{c:d}.ome.tif", "", "NG_Zarr", ""),  # empty out_img_name
        (
            "img_r{r:d}_c{c:d}.ome.tif",
            "output_image",
            "tiff",
            "",
        ),  # invalid output format
        (
            "img_r{r:d}_c{c:d}.ome.tif",
            "output_image",
            "NG_Zarr",
            '{0:"max"}',
        ),  # invalid downsample method
    ],
)
def test_param_parsing_image_collection(
    filename_pattern,
    out_img_name,
    output_format,
    downsample_method,
    gen_image_collection,
):
    """Test command line argument parsing for image collection.

    All tests are expected to raise ValueError.
    """
    input_path, _, _, _ = gen_image_collection

    with pytest.raises(ValueError):
        _, _ = _validate_params(
            input_path, filename_pattern, out_img_name, output_format, downsample_method
        )  # use default downsample method
