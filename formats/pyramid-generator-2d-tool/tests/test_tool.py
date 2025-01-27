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
def gen_data_path() -> typing.Generator[Path, None, None]:
    """Generate a temporary path holding test data."""
    data_path = Path("data")
    data_path.mkdir(parents=True, exist_ok=True)

    yield data_path

    # delete the temporary path
    shutil.rmtree(data_path)


@pytest.fixture
def gen_single_image_path(
    gen_data_path,
) -> typing.Generator[typing.Tuple[Path, Path], None, None]:
    """Generate input and output path for single image test."""
    data_path = gen_data_path
    inp_dir = data_path / "input/single_image"
    inp_dir.mkdir(parents=True, exist_ok=True)

    out_dir = data_path / "output/single_image"
    out_dir.mkdir(parents=True, exist_ok=True)

    yield inp_dir, out_dir

    # delete the input and output path
    shutil.rmtree(inp_dir)
    shutil.rmtree(out_dir)


@pytest.fixture
def gen_single_image(
    gen_single_image_path,
) -> typing.Generator[typing.Tuple[Path, Path], None, None]:
    """Create a single image."""
    inp_dir, out_dir = gen_single_image_path

    # img_path = _gen_random_img(inp_dir, "random_img.tif", 2048)
    img_path = _get_real_img(inp_dir)

    yield img_path, out_dir

    # delete the image
    img_path.unlink()


@pytest.fixture
def gen_image_collection_path(
    gen_data_path,
) -> typing.Generator[typing.Tuple[Path, Path], None, None]:
    """Generate input and output path for image collection test."""
    data_path = gen_data_path
    inp_dir = data_path / "input/image_collection"
    inp_dir.mkdir(parents=True, exist_ok=True)

    out_dir = data_path / "output/image_collection"
    out_dir.mkdir(parents=True, exist_ok=True)

    yield inp_dir, out_dir

    # delete the input and output path
    shutil.rmtree(inp_dir)
    shutil.rmtree(out_dir)


@pytest.fixture
def gen_image_collection(
    gen_image_collection_path,
) -> typing.Generator[typing.Tuple[Path, Path, str, str], None, None]:
    """Create an image collection."""
    inp_dir, out_dir = gen_image_collection_path

    img_paths = []
    for i in range(4):
        img_path = _get_real_img(inp_dir, f"img_r001_c{i:03d}.ome.tif")
        img_paths.append(img_path)

    file_pattern = "img_r001_c{c:ddd}.ome.tif"
    out_img_name = "output_img"
    yield inp_dir, out_dir, file_pattern, out_img_name

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
    inp_dir, out_dir = gen_single_image
    min_dim, out_format, ds_dict = gen_process_params

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inpDir",
            str(inp_dir),
            "--outDir",
            str(out_dir),
            "--minDim",
            min_dim,
            "--outFormat",
            out_format,
            "--dsMethod",
            ds_dict,
        ],
    )

    # Test for a successful run
    assert result.exit_code == 0


def test_cli_out_format(gen_single_image):
    """Test output format for the command line.

    Test with invalid output format. Expected nonzero error code.
    """
    inp_dir, out_dir = gen_single_image
    min_dim = 128
    ds_dict = '{0: "mean"}'
    invalid_format = "invalid_format"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inpDir",
            str(inp_dir),
            "--outDir",
            str(out_dir),
            "--minDim",
            min_dim,
            "--outFormat",
            invalid_format,
            "--dsMethod",
            ds_dict,
        ],
    )

    # expected error
    assert result.exit_code != 0


@pytest.mark.skip(reason="Image collection set seems to need stitching vector")
def test_cli_image_collection(gen_image_collection):
    """Test the command line."""
    inp_dir, out_dir, file_pattern, out_img_name = gen_image_collection
    # min_dim, out_format, ds_dict = gen_process_params
    min_dim = 128
    out_format = "NG_Zarr"
    ds_dict = '{0: "mean"}'
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inpDir",
            str(inp_dir),
            "--outDir",
            str(out_dir),
            "--filePattern",
            file_pattern,
            "--outImgName",
            out_img_name,
            "--minDim",
            min_dim,
            "--outFormat",
            out_format,
            "--dsMethod",
            ds_dict,
        ],
    )

    # Test for a successful run
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "file_pattern,out_img_name,ds_method",
    [
        ("", "output_image", ""),  # empty file pattern
        ("img_r{r:d}_c{c:d}.ome.tif", "", ""),  # empty out_img_name
        (
            "img_r{r:d}_c{c:d}.ome.tif",
            "output_image",
            '{0:"max"}',
        ),  # invalid downsample method
    ],
)
def test_param_parsing_image_collection(
    file_pattern,
    out_img_name,
    ds_method,
    gen_image_collection,
):
    """Test command line argument parsing for image collection.

    All tests are expected to raise ValueError.
    """
    inp_dir, _, _, _ = gen_image_collection

    with pytest.raises(ValueError):
        _, _ = _validate_params(
            inp_dir, file_pattern, out_img_name, ds_method
        )  # use default downsample method
