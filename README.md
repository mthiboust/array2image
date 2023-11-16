# Array2image

***Array2image*** helps you convert Numpy arrays to PIL images. It comes with a single function `array_to_image()`.

When given an array, it automatically guesses its spatial and channel dimensions. Images are then represented differently depending on the channel dimension:
* 1D channel: greyscale image.
* 2D channel: color image with varying hue and saturation.
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

<table>
<tr>
<td>

```python
from array2image import array_to_image
import matplotlib
import numpy as np

# 8x8 Numpy array with random values between 0 and 1
array = np.random.uniform(0,1,(8,8))

array_to_image(array)
```

</td>
<td> 
<img src="https://github.com/mthiboust/array2image/blob/ec7b667c2048a8b85500beeb86442589dee8167a/docs/default.png">
</td>
</tr>

<tr>
<td>

```python
from array2image import array_to_image
import matplotlib
import numpy as np

# 8x8 Numpy array with random values between 0 and 1
array = np.random.uniform(0,1,(8,8))

array_to_image(array, inverted_colors=True)
```

</td>
<td> 
<img src="https://raw.githubusercontent.com/mthiboust/colormap2d/dev/docs/inverted.png">
</td>
</tr>

</table>



