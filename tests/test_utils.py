"""Tests the plotting utility functions."""

# ruff: noqa: D103

from array2image.core import _grid_image, _guess_spatial_channel_dims, array_to_image


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
