# Array2image

***Array2image*** helps you convert Numpy arrays to PIL images. It comes with a single function `array_to_image()`.

When given an array, it automatically guesses its spatial and channel dimensions. Spatial dimensions greater than 2 are considered as images of images. The resulting image is then represented differently depending on the channel dimension:
* 1D channel: greyscale image.
* 2D channel: image with varying hue and saturation.
* 3D channel: RGB image.

If specified, custom colormap functions can be used instead. For instance:
* `matplotlib.cm.*` functions for 1D channel arrays (like `matplotlib.cm.viridis`)
* `colormap2d.*` functions for 2D channel arrays (like `colormap2d.pinwheel`)
* The `matplotlib.colors.hsv_to_rgb` function for 3D channel arrays.`

It assumes that values are floats between 0 and 1 or integers between 0 and 255 (values are clipped anyway). If specified, it automatically normalizes the values.

Why not directly use `matplotlib.plt.imshow` instead? If you have 2D array with 1 or 3-channel data and don't care about the size nor the incrusted axis in the returned image, `matplotlib.plt.imshow` is great. The ***Array2image*** library makes the focus on simplicity by guessing an appropriate way of rendering non-generic arrays. 

# Installation

```bash
pip install array2image
```

Requires python 3.10+.

# Documentation

### Function signature
```python
def array_to_image(
    arr,
    spatial_dims: tuple[int, ...] | None = None,
    channel_dim: int | None = None,
    cmap: Callable | None = None,
    inverted_colors: bool = False,
    bin_size: int | tuple[int, int] | None = None,
    target_total_size: int = 200,
    grid_thickness: int | tuple[int, ...] = 0,
    norm: bool = False,
) -> PIL.Image
```

### Argument description

* **arr**: Array-like to be converted.
* **spatial_dims**: Spatial dimensions of the array. If None, spatial dimensions are
automatically guessed.
* **channel_dim**: Channel dimension of the array. Only 1, 2 or 3 channel dimension
arrays can be converted to an image. If None, the channel dimension is
automatically guessed.
* **cmap**: Colormap function to be used if provided. If None, default built-in
functions are used.
* **inverted_colors**: If True, inverts the color of the image.
* **bin_size**: Number of pixels for each array spatial element.
target_total_size: Target size of the image. Used to automatically choose
`bin_size` if the latter is None.
* **grid_thickness**: Tuple of grid thickness for each level of 2D spatial dimensions.
By default, it is 0 for the last 2D dimensions and 2 pixels for the others.
* **norm**: If True, normalize values between 0 and 1 with a min-max normalization.

# Examples

## 1-channel arrays

Data for the following examples:
```python
import numpy as np

# Random data: A 2x4x10x8 Numpy array with random values between 0 and 1
np.random.seed(0)
array = np.random.uniform(0, 1, (2, 4, 10, 8))

# MNIST data: The first 48 MNIST digits organized in a 6x8 grid.
mnist_data = ...
array = mnist_data[:48].reshape(6, 8, 28, 28)
```

<table>
<tr>
<td>
</td>
<td>Random</td>
<td>MNIST</td>
</tr>
<tr>
<td>

```python
from array2image import array_to_image

# Represent only a 4D array
image = array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_random.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_mnist_6_8_28_28.png" width="200px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Force 0 pixel for all grid levels
image = array_to_image(
  array, 
  grid_thickness=(0, 0)
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_random_grid_0_0.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_mnist_6_8_28_28_grid_0_0.png" width="200px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Invert colors
image = array_to_image(
  array, 
  inverted_colors=True
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_random_grid_0_0_inverted_colors.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_mnist_6_8_28_28_inverted_colors.png" width="200px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# Use an external colormap
image = array_to_image(
  array,
  cmap=matplotlib.cm.viridis
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_random_grid_0_0_cmap_viridis.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8b448f9e3a55961c31c6035a365c9a03d56482d6/docs/a2i_mnist_6_8_28_28_cmap_viridis.png" width="200px">
</td>
</tr>
<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# Represent only a 2D array
image = array_to_image(
  array[0, 0], 
  cmap=matplotlib.cm.viridis
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_random_0_0_cmap_viridis.png">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_mnist_28_28.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# Show a grid
image = array_to_image(
  array[0, 0], 
  cmap=matplotlib.cm.viridis, 
  grid_thickness=1
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_random_0_0_cmap_viridis_grid_1.png">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_mnist_28_28_grid_1.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Fix the bin size
image = array_to_image(
  array[0, 0], 
  bin_size=4
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_random_0_0_bin_2.png">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_mnist_28_28_grid_1_bin_4.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Fix a specific asymetric bin size
image = array_to_image(
  array[0, 0], 
  bin_size=(4,8)
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_random_0_0_bin_2_4.png">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/9b25a4e2db5db8402058b9f6651894b82cf264ce/docs/a2i_mnist_28_28_grid_1_bin_4_8.png">
</td>
</tr>
</table>

## 2-channel arrays


Data for the following examples:
```python
import numpy as np

# Random data: A 10x10x2 Numpy array with random values between 0 and 1
np.random.seed(0)
array = np.random.uniform(0, 1, (10, 10, 2))

# Dummy fourier data: linearly varying phase and magnitude over a 2D grid
phase, amplitude = np.meshgrid(np.linspace(0,1,10), np.meshgrid(np.linspace(0,1,10)))
array = np.stack((phase, amplitude), axis=-1)
```

<table>
<tr>
<td>
</td>
<td>Random</td>
<td>Fourier</td>
</tr>
<tr>
<td>

```python
from array2image import array_to_image

# Default Hue/Saturation colormap
image = array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/072db6c96721efcdc0171b4d579679786b456f69/docs/a2i_2c_random.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/072db6c96721efcdc0171b4d579679786b456f69/docs/a2i_2c_fourier.png" width="200px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import colormap2d

# External 2D colormap
array_to_image(
  array, 
  cmap=colormap2d.pinwheel
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/072db6c96721efcdc0171b4d579679786b456f69/docs/a2i_2c_random_cmap.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/072db6c96721efcdc0171b4d579679786b456f69/docs/a2i_2c_fourier_cmap.png" width="200px">
</td>
</tr>

</table>

## 3-channel arrays

Data for the following examples:
```python
import numpy as np

# Random data: A 10x10x3 Numpy array with random values between 0 and 1
np.random.seed(0)
array = np.random.uniform(0, 1, (10, 10, 3))

# The Lena RGB image
image = Image.open("lena.png")
array = np.asarray(image)
```

<table>
<tr>
<td>
</td>
<td>Random</td>
<td>Lena</td>
</tr>
<tr>
<td>

```python
from array2image import array_to_image

# Default RGB colormap
image = array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/4eedddcd31a63ed7f9f893cb474a99b89c555642/docs/a2i_3c_random.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/4eedddcd31a63ed7f9f893cb474a99b89c555642/docs/a2i_3c_lena.png" width="200px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# External 3D colormap
array_to_image(
  array, 
  cmap=matplotlib.colors.hsv_to_rgb
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/4eedddcd31a63ed7f9f893cb474a99b89c555642/docs/a2i_3c_random_cmap.png" width="200px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/4eedddcd31a63ed7f9f893cb474a99b89c555642/docs/a2i_3c_lena_cmap.png" width="200px">
</td>
</tr>

</table>