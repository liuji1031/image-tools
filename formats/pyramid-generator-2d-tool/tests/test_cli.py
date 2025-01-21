"""Testing the Command Line Tool."""

import faulthandler
from pathlib import Path

import bfio
import numpy as np
import pytest
import requests
from polus.images.formats.pyramid_generator_2d.__main__ import app
from typer.testing import CliRunner

faulthandler.enable()


# SINGLE_IMG_PARAMS =


def _get_real_img(path2save: Path):
    """Download a real image from the internet.

    Args:
        path2save (Path): path to save the image

    Returns:
        str : path to the downloaded image
    """
    # Download the data if it doesn't exist
    URL = "https://github.com/usnistgov/WIPP/raw/master/data/PyramidBuilding/inputCollection/"
    filename = "img_r001_c001.ome.tif"
    if not (path2save / filename).exists():
        content = requests.get(URL + filename, timeout=10.0).content
        (path2save / filename).open("wb").write(content)

    return str(path2save / filename)


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
def gen_single_image():
    """Create a single image."""
    # download a sample image
    input_path = Path("data/input/single_image")
    input_path.mkdir(parents=True, exist_ok=True)

    output_path = Path("data/output/single_image")
    output_path.mkdir(parents=True, exist_ok=True)

    # img_path = _gen_random_img(input_path, "random_img.tif", 2048)
    img_path = _get_real_img(input_path)

    return img_path, str(output_path)


@pytest.fixture(
    params=[[128, "NG_Zarr", '{0: "mean"}'], [128, "Viv", '{0: "mean"}']],
    ids=["128_NG_Zarr", "128_Viv"],
)
def gen_single_image_params(request):
    """Return the default parameters for the single image."""
    return request.param


def test_cli_single_img(gen_single_image, gen_single_image_params):
    """Test the command line."""
    input_path, output_path = gen_single_image
    min_dim, output_format, downsample_dict = gen_single_image_params

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inputPath",
            input_path,
            "--outputPath",
            output_path,
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


def test_cli_parsing():
    """Test command line argument parsing."""
