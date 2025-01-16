"""Tests for pyramid-generator-2d."""

import pytest


def test_pyramid_generator_2d():
    """Test pyramid-generator-2d."""
    # TODO: Add tests


@pytest.mark.skipif("not config.getoption('slow')")
def test_slow_pyramid_enerator_2d():
    """Test that can take a long time to run."""
    # TODO: Add optional tests


@pytest.mark.skipif("not config.getoption('downloads')")
def test_download_pyramid_generator_2d():
    """Test thatdownload data from."""
    # TODO: Add optional tests
