"""Utility functions for plotting SOMs."""

import logging
from collections.abc import Callable

import numpy as np
from PIL import Image


def _grid_image(
    shape: tuple[int, int], patch_shape: tuple[int, int], thickness: int = 1
) -> Image:
    """Returns a RGBA PIL image containing a white grid on a transparent background.

    Args:
        shape: Width and height of the image.
        patch_shape: Size of each grid element.
        thickness: Thickness of the grid lines.

    Returns:
        A PIL image with a white grid on a transparent background.
    """
    y, x = shape
    p_y, p_x = patch_shape

    if min(p_x, p_y) < 3:
        raise ValueError(
            f"Patches of shape {patch_shape} are too small to be overlapped by a grid."
        )

    arr = np.zeros((x, y, 4))

    # Add horizontal bands
    for i in range(0, x // p_x + 1):
        k = i * p_x
        arr[np.maximum(k - thickness, 0) : np.minimum(k + thickness, x), :, :] = 1

    # Add vertical bands
    for i in range(0, y // p_y + 1):
        k = i * p_y
        arr[:, np.maximum(k - thickness, 0) : np.minimum(k + thickness, y), :] = 1

    return Image.fromarray(np.uint8(arr * 255), "RGBA")


def _guess_spatial_channel_dims(shape: tuple[int, ...]) -> tuple[tuple[int], int]:
    """Guesses the spatial and channel dimensions of an array shape.

    Example:
        ```python
        _guess_spatial_channel_dims((1,)) # ((1,), 1)
        _guess_spatial_channel_dims((8,)) # ((8,), 1)
        _guess_spatial_channel_dims((8,8)) # ((8, 8), 1)
        _guess_spatial_channel_dims((8,8,1)) # ((8, 8), 1)
        _guess_spatial_channel_dims((8,8,3)) # ((8, 8), 3)
        _guess_spatial_channel_dims((8,8,4)) # ((8, 8, 4), 1)

        # A 3x3 array can be ambiguous because it could mean either:
        # * a list of 3 RGB values (default guess)
        # * a 3x3 greyscale image (need to reshape to (3,3,1) for this behavior)
        _guess_spatial_channel_dims((3,3)) # ((3,), 3)
        _guess_spatial_channel_dims((3,3,1)) # ((3, 3), 1)
        ```

    Args:
        shape: Shape of the array.

    Returns:
        Spatial dimensions (tuple).
        Channel dimension (int).
    """
    match shape:
        case (*s, c) if c <= 3 and len(s) > 0:
            spatial_dims, channel_dim = tuple(s), c
        case _:
            spatial_dims, channel_dim = shape, 1
    return spatial_dims, channel_dim


def array_to_image(
    arr: np.array,
    spatial_dims: tuple[int] | tuple[int, int] | None = None,
    channel_dim: int | None = None,
    colormap: Callable | None = None,
    inverted_colors: bool = False,
    zoom_factor: int | tuple[int, int] | None = None,
    show_grid: bool = False,
    min_max_normalization: bool = False,
) -> Image:
    """Converts an array-like to a PIL image.

    Useful function to get an overview of a 2D array containing a 1D/2D/3D channel.
    Values are represented differently depending on the channel dimension:
    * 1D channel: greyscale image.
    * 2D channel: color image with varying hue and saturation.
    * 3D channel: RGB image.

    If specified, custom colormap functions can be used instead. For instance:
    * `matplotlib.cm.*` functions for 1D channel arrays (like `matplotlib.cm.viridis`)
    * `colormap2d.*` functions for 2D channel arrays (like `colormap2d.pinwheel`)

    Assumes that values are floats between 0 and 1 (values are clipped anyway).

    Args:
        arr: Array to be converted.
        spatial_dims: Spatial dimensions of the array. Only 1 or 2 spatial dimension
            arrays can be converted to an image.
        channel_dim: Channel dimension of the array. Only 1, 2 or 3 channel dimension
            arrays can be converted to an image.
        colormap: Colormap function to be used instead of the built-in functions.
        inverted_colors: If True, inverts the color of the image.
        zoom_factor: Number of pixels for each array spatial element.
        show_grid: If True, adds a grid to separate the representation of each element.
        min_max_normalization: If True, normalize the values between 0 and 1.
    """
    if min_max_normalization:
        min_val = arr.min()
        max_val = arr.max()
        arr = (arr - min_val) / (max_val - min_val)

    elif not np.issubdtype(arr.dtype, np.floating):
        logging.info(
            "The array values are not float numbers. "
            "Values are expected to be in the [0:1] range to be converted to an image."
            "You may want to use the `min-max-normalization=True` argument instead."
        )

    elif arr.min() < 0 or arr.max() > 1:
        logging.warning(
            "Clipping values not in the [0:1] range. "
            "You may want to use the `min-max-normalization=True` argument instead."
        )
        arr = np.clip(arr, 0.0, 1.0)

    if inverted_colors:
        arr = 1 - arr

    # Try to guess the spatial and channel dim to represent the data
    if spatial_dims is None or channel_dim is None:
        spatial_dims, channel_dim = _guess_spatial_channel_dims(arr.shape)

    if len(spatial_dims) == 1:
        spatial_dims = (1,) + spatial_dims
    elif len(spatial_dims) > 2:
        raise ValueError("Could not represent array of more than 2 spatial dimensions.")

    # Force a 3D array with 2 spatial dimensions and 1 channel dimension
    arr = arr.reshape(spatial_dims + (channel_dim,))
    assert len(arr.shape) == 3

    if colormap is not None:
        arr = colormap(arr)
        img = Image.fromarray(np.uint8(arr * 255), "RGBA")

    else:
        match channel_dim:
            case 1:
                img = Image.fromarray(np.uint8(arr.squeeze() * 255), "L")

            case 2:
                # Increase the channel from 2 to 3 by padding with 1s.
                arr = np.concatenate((arr, np.ones(spatial_dims + (1,))), axis=-1)
                img = Image.fromarray(np.uint8(arr * 255), "HSV")
                img = img.convert("RGB")

            case 3:
                img = Image.fromarray(np.uint8(arr * 255), "RGB")

            case _:
                raise ValueError(
                    f"Cannot represent `channel_dim` of {channel_dim}."
                    f"Possible values: 1, 2 or 3"
                )

    dim_x, dim_y = arr.shape[:2]

    if zoom_factor is None:
        # Try to guess a convenient scale_factor
        IMG_COMMON_DIMENSION = 200
        zoom_factor = max(1, IMG_COMMON_DIMENSION // max(dim_x, dim_y))

    if isinstance(zoom_factor, int):
        zoom_factor = (zoom_factor, zoom_factor)

    img = img.resize((dim_y * zoom_factor[0], dim_x * zoom_factor[1]), Image.NEAREST)

    if show_grid:
        grid_image = _grid_image(img.size, zoom_factor, thickness=1)
        img.paste(grid_image, (0, 0), mask=grid_image)

    return img
