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

```python
from array2image import array_to_image

array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_default.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

array_to_image(array, inverted_colors=True)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_inverted_colors.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Values are automatically clipped to the [0:1] range
overlimit_array = array * 2
image = array_to_image(overlimit_array, inverted_colors=True)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/52b3dd5e9e48ff3c4064aeb30ac6e7ed3c41a261/docs/a2i_2s1c_overlimit.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image

# Values are automatically clipped to the [0:1] range
overlimit_array = array * 2
image = array_to_image(overlimit_array, inverted_colors=True,min_max_normalization=True)
```

</td>
<td> 
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib

image = array_to_image(array, colormap=matplotlib.cm.viridis)
```

</td>
<td> 
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
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
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
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
  zoom_factor=10
  )

```

</td>
<td> 
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
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
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
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
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
</td>
</tr>

</table>



