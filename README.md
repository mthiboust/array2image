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

# Examples

## 1-channel arrays

Generate some data:
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
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
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
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_inverted_colors.png" width="100px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
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
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_overlimit.png" width="100px">
</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
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
<img src="https://github.com/mthiboust/array2image/blob/8cf3a47b42b650b219326f5b83706a39c3fc090e/docs/a2i_2s1c_overlimit_norm.png" width="100px">
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
<img src="https://github.com/mthiboust/array2image/blob/a805d35042cbc37bd36f9db9e895b7a018be95fb/docs/a2i_2s1c_colormap_magma.png" width="100px">
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
<img src="https://github.com/mthiboust/array2image/blob/8cf3a47b42b650b219326f5b83706a39c3fc090e/docs/a2i_2s1c_colormap_viridis.png" width="100px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# Fix the bin size
image = array_to_image(
  array[0, 0], 
  bin_size=4
)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8cf3a47b42b650b219326f5b83706a39c3fc090e/docs/a2i_2s1c_colormap_viridis_show_grid.png" width="100px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

# Fix a specific asymetric bin size
image = array_to_image(
  array[0, 0], 
  bin_size=(4,8)
)
```

</td>
</tr>
</table>

## 2-channel arrays

## 3-channel arrays

