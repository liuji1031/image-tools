"""Testing the Command Line Tool."""

import faulthandler
from pathlib import Path

from polus.images.formats.pyramid_generator_2d.__main__ import app
from typer.testing import CliRunner

faulthandler.enable()


def test_cli():
    """Test the command line."""
    # TODO: Set up parameters for the test
    (
        inp_dir,
        out_dir,
    ) = Path(
        "tests/data/inp"
    ), Path("tests/data/out")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--inpDir",
            inp_dir,
            "--outDir",
            out_dir,
        ],
    )

    # Test for a successful run
    assert result.exit_code == 0

    # TODO: Add more tests
