"""Tests the plotting utility functions.

Todo:
* array_to_image tests
* add_grid tests
"""

# ruff: noqa: D103

import numpy as np
from array2image.core import _add_grid, _guess_spatial_channel_dims, array_to_image


def test_guess_spatial_channel_dimensions():
    assert _guess_spatial_channel_dims((1,)) == ((1,), 1)
    assert _guess_spatial_channel_dims((8,)) == ((8,), 1)
    assert _guess_spatial_channel_dims((8, 8)) == ((8, 8), 1)
    assert _guess_spatial_channel_dims((8, 8, 1)) == ((8, 8), 1)
    assert _guess_spatial_channel_dims((8, 8, 3)) == ((8, 8), 3)
    assert _guess_spatial_channel_dims((8, 8, 4)) == (
        (8, 8, 4),
        1,
    )

    assert _guess_spatial_channel_dims((3, 3)) == ((3,), 3)
    assert _guess_spatial_channel_dims((3, 3, 1)) == ((3, 3), 1)


def test_array_to_image():
    array = np.ones((10, 10, 1))
    array_to_image(array)


def test_add_grid():
    array = np.ones((10, 10, 1))
    _add_grid(array, spacing=1, thickness=1)
