"""Array2image."""

import logging
from collections.abc import Callable

import numpy as np
from PIL import Image


def _ensure_tuple(x):
    if isinstance(x, tuple) and len(x) == 2:
        return x
    elif isinstance(x, int):
        return (x, x)
    else:
        raise ValueError(
            f"Type of {x} should be either `int` or `tuple[int, int]`, not {type(x)}."
        )


def _add_grid(
    arr: np.ndarray,
    spacing: int | tuple[int, int],
    thickness: int | tuple[int, int] = 1,
    color: float = 1.0,
) -> np.ndarray:
    """Adds a grid to an array.

    The spacing parameter should be a divisor of the array spatial dimensions.

    Args:
        arr: Numpy array whose last 3 dimensions are spatial (x, y) and channel (c).
        spacing: Spacing to be applied. Must be a divisor of the array spatial dims.
        thickness: Thickness of the grid line.
        color: Color of the grid line. White is 1, black is 0.

    Returns:
        An array with modified spatial dimensions.
    """
    *s, x, y, c = arr.shape
    sx, sy = _ensure_tuple(spacing)
    tx, ty = _ensure_tuple(thickness)

    if x % sx != 0 or y % sy != 0:
        raise ValueError(f"{x} (resp {y}) should be divisible by {sx} (resp {sy}).")

    arr = arr.reshape(tuple(s) + (x // sx, sx, y // sy, sy, c))

    # Add the internal grid, including the trailing vertical and horizontal lines.
    pad_width = [(0, 0) for i in range(arr.ndim)]
    pad_width[-4] = (0, tx)
    pad_width[-2] = (0, ty)
    pad_width = tuple(pad_width)
    arr = np.pad(arr, pad_width, mode="constant", constant_values=color)

    arr = arr.reshape(tuple(s) + ((x // sx) * (sx + tx), (y // sy) * (sy + ty), c))

    # Add the missing leading vertical and horizontal lines.
    pad_width = [(0, 0) for i in range(arr.ndim)]
    pad_width[-3] = (tx, 0)
    pad_width[-2] = (ty, 0)
    pad_width = tuple(pad_width)
    arr = np.pad(arr, pad_width, mode="constant", constant_values=color)

    return arr


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
        A tuple of the spatial dimensions (tuple) and the channel dimension (int).
    """
    match shape:
        case (*s, c) if c <= 3 and len(s) > 0:
            spatial_dims, channel_dim = tuple(s), c
        case _:
            spatial_dims, channel_dim = shape, 1
    return spatial_dims, channel_dim


def array_to_image(
    arr,
    spatial_dims: tuple[int] | tuple[int, int] | None = None,
    channel_dim: int | None = None,
    cmap: Callable | None = None,
    inverted_colors: bool = False,
    bin_size: int | tuple[int, int] | None = None,
    target_total_size: int = 200,
    grid_thickness: int | tuple[int, ...] = 0,
    norm: bool = False,
) -> Image:
    """Converts an array-like to a PIL image.

    Visualization function to get a quick overview of a 2D/4D/nD array containing a
    1D/2D/3D channel.

    When given an array, it automatically guesses its spatial and channel dimensions.
    Spatial dimensions greater than 2 are considered as images of images. The resulting
    image is then represented differently depending on the channel dimension:
    * 1D channel: greyscale image.
    * 2D channel: image with varying hue and saturation.
    * 3D channel: RGB image.

    If specified, custom colormap functions can be used instead. For instance:
    * `matplotlib.cm.*` functions for 1D channel arrays (like `matplotlib.cm.viridis`)
    * `colormap2d.*` functions for 2D channel arrays (like `colormap2d.pinwheel`)
    * The `matplotlib.colors.hsv_to_rgb` function for 3D channel arrays.`

    It assumes that values are floats between 0 and 1 or integers between 0 and 255
    (values are clipped anyway). If specified, it automatically normalizes the values.

    Args:
        arr: Array-like to be converted.
        spatial_dims: Spatial dimensions of the array. If None, spatial dimensions are
            automatically guessed.
        channel_dim: Channel dimension of the array. Only 1, 2 or 3 channel dimension
            arrays can be converted to an image. If None, the channel dimension is
            automatically guessed.
        cmap: Colormap function to be used if provided. If None, default built-in
            functions are used.
        inverted_colors: If True, inverts the color of the image.
        bin_size: Number of pixels for each array spatial element.
        target_total_size: Target size of the image. Used to automatically choose
            `bin_size` if the latter is None.
        grid_thickness: Tuple of grid thickness for each level of 2D spatial dimensions.
            By default, it is 0 for the last 2D dimensions and 2 pixels for the others.
        norm: If True, normalize values between 0 and 1 with a min-max normalization.
    """
    arr = np.asarray(arr)

    if np.issubdtype(arr.dtype, np.integer):
        arr = arr / 255

    if not np.issubdtype(arr.dtype, np.floating):
        raise TypeError(
            "The array values should be either floats between 0 and 1, or integers "
            "between 0 and 255."
        )

    if norm:
        min_val = arr.min()
        max_val = arr.max()
        arr = (arr - min_val) / (max_val - min_val)

    elif arr.min() < 0 or arr.max() > 1:
        logging.warning(
            "Clipping values not in the [0:1] range. "
            "You may want to use the `norm=True` argument."
        )
        arr = np.clip(arr, 0.0, 1.0)

    if inverted_colors:
        arr = 1 - arr

    # Try to guess the spatial and channel dim to represent the data
    if spatial_dims is None or channel_dim is None:
        spatial_dims, channel_dim = _guess_spatial_channel_dims(arr.shape)

    # Make sure that the number of spatial dims is a multiple of 2
    if len(spatial_dims) % 2 == 1:
        spatial_dims = (1,) + spatial_dims

    if channel_dim > 3:
        raise ValueError(
            f"Cannot represent `channel_dim` of {channel_dim}."
            f"Possible values: 1, 2 or 3"
        )

    # Force a 3D array with 2 spatial dimensions and 1 channel dimension
    arr = arr.reshape(spatial_dims + (channel_dim,))
    # assert len(arr.shape) == 3

    # print(f"before colormap: {arr.shape=}")
    if cmap is not None:
        _shape = arr.shape
        if channel_dim == 1:
            # Matplotlib colormap functions need no channel dimension
            arr = arr.squeeze(axis=-1)

        # Apply colormap and make sure to only keep 3 channels
        # (matplotlib colormap functions returns 4 channels RGBA).
        arr = cmap(arr)

        if len(arr.shape) > len(_shape):
            raise ValueError(
                "The colormap function has changed the number of dimensions "
                f"of the array from {_shape} to {arr.shape}. "
                "Make sure this colormap function is adapted to array with a "
                f"channel dimension of {channel_dim}."
            )

    elif cmap is None and channel_dim == 2:
        # Add a third channel filled with 1s and consider those values as HSV values.
        arr = np.concatenate((arr, np.ones(spatial_dims + (1,))), axis=-1)
        arr = matplotlib.colors.hsv_to_rgb(arr)

    if bin_size is None:
        # Try to guess a convenient scale_factor
        x_charac = int(np.prod(spatial_dims[::2]))
        y_charac = int(np.prod(spatial_dims[1::2]))
        bin_size = max(1, target_total_size // max(x_charac, y_charac))

    bin_size = _ensure_tuple(bin_size)

    if bin_size != (1, 1):
        # Rescale each value to a bin of bin_size[0]*bin_size[1] pixels.
        *s, x, y, c = arr.shape
        arr = arr.reshape(tuple(s) + (x, 1, y, 1, c))
        arr = arr * np.ones(tuple(s) + (x, bin_size[0], y, bin_size[1], c))
        arr = arr.reshape(tuple(s) + (x * bin_size[0], y * bin_size[1], c))

    # Set default grid thicknesses for all levels if not provided
    grid_thickness = (
        [grid_thickness] if isinstance(grid_thickness, int) else list(grid_thickness)
    )

    while len(grid_thickness) < len(spatial_dims) // 2:
        grid_thickness.insert(0, max(2, grid_thickness[0]))

    if (thickness := grid_thickness.pop()) != 0:
        arr = _add_grid(arr, bin_size, thickness)

    # If array has more than 3 spatial dimensions, iterate to make images of images
    while len(arr.shape) >= 5:
        *s, xx, yy, x, y, c = arr.shape

        arr = arr.swapaxes(-4, -3)
        arr = arr.reshape(tuple(s) + (xx * x, yy * y, c))

        if (thickness := grid_thickness.pop()) != 0:
            arr = _add_grid(arr, (x, y), thickness)

    # Return the corresponding PIL image
    match arr.shape[-1]:
        case 1:
            return Image.fromarray(np.uint8(arr.squeeze(axis=-1) * 255), "L")
        case 3:
            return Image.fromarray(np.uint8(arr * 255), "RGB")
        case 4:
            return Image.fromarray(np.uint8(arr * 255), "RGBA")
        case _:
            raise ValueError(f"{arr.shape=}")
