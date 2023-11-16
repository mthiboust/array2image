# Array2image

***Array2image*** helps you convert Numpy arrays to PIL images. It comes with a single function `array_to_image()`.

When given an array, it automatically guesses its spatial and channel dimensions. Images are then represented differently depending on the channel dimension:
* 1D channel: greyscale image.
* 2D channel: image with varying hue and saturation.
* 3D channel: RGB image.

If specified, custom colormap functions can be used instead. For instance:
* `matplotlib.cm.*` functions for 1D channel arrays (like `matplotlib.cm.viridis`)
* `colormap2d.*` functions for 2D channel arrays (like `colormap2d.pinwheel`)

It assumes that values are floats between 0 and 1 (values are clipped anyway). You can also automatically normalize the values.

# Installation

```bash
pip install array2image
```

Requires python 3.10+.

# Usage

## 1-channel arrays

Generate some data:
```python
import numpy as np

# 8x8 Numpy array with random values between 0 and 1
np.seed(0)
array = np.random.uniform(0,1,(8,8))
```

<table>
<tr>
<td>
</td>
<td>Random</td>
<td>Digit</td>
<td>Digit * 2</td>
</tr>
<tr>
<td>

```python
from array2image import array_to_image

image = array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png" width="100px">
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

array_to_image(
  array, 
  inverted_colors=True
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

# Values are automatically clipped 
# to the [0:1] range
overlimit_array = array * 2
image = array_to_image(
  overlimit_array, 
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

# Values are automatically clipped 
# to the [0:1] range
overlimit_array = array * 2
image = array_to_image(
  overlimit_array, 
  inverted_colors=True,
  min_max_normalization=True
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

image = array_to_image(
  array, 
  colormap=matplotlib.cm.magma
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

image = array_to_image(
  array, 
  colormap=matplotlib.cm.viridis
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

image = array_to_image(
  array, 
  colormap=matplotlib.cm.viridis, 
  show_grid=True
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

image = array_to_image(
  array, 
  colormap=matplotlib.cm.viridis, 
  show_grid=True, 
  zoom_factor=5
  )

```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/8cf3a47b42b650b219326f5b83706a39c3fc090e/docs/a2i_2s1c_colormap_viridis_show_grid_zoom5.png" width="100px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

image = array_to_image(
  array, 
  colormap=matplotlib.cm.viridis, 
  show_grid=True, 
  zoom_factor=30
  )
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/95f81b8400add48e156725d02f99b72d4d470a2a/docs/a2i_2s1c_colormap_viridis_show_grid_zoom30.png" width="100px">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

image = array_to_image(
  array, 
  colormap=matplotlib.cm.viridis, 
  show_grid=True, 
  zoom_factor=(20, 10)
  )
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/95f81b8400add48e156725d02f99b72d4d470a2a/docs/a2i_2s1c_colormap_viridis_show_grid_zoom2010.png" width="100px">
</td>
</tr>

</table>

## 2-channel arrays

## 3-channel arrays

