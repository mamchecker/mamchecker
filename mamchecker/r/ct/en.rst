.. raw:: html

    %path = "maths/direction"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->

Two different variables, for which all combinations are possible can be called
orthogonal.  They generate the maximal set of combinations (area).  The vector
product is maximal, the dot product 0.

Variables, one normally deals with, are extensive quantities and not points. 
3m means all points from 0 to 3m.

A 2D vector `\mathbf{v}` and `z\in\mathbb{C}` are such extensive quantities.
The created area is `\mathbf{v_1}\times\mathbf{v_2}` or `Im(z_1\bar{z_2})`.

Quantities that show to the same direction can be added.
Different directions can be added component-wise.

- `\frac{\mathbf{v_1}\mathbf{v_2}}{|\mathbf{v_1}|}=\mathbf{v_1}_0\mathbf{v_2}` 
  is the component of `\mathbf{v_2}`, that can be added to `\mathbf{v_1}`.

- `\frac{z_1\bar{z_2}}{|z_1|}` is the complex number with real part parallel to `z_1`
  and imaginary part orthogonal to `z_1`. Normally you would simply do `z_1+z_2`,
  i.e. calculate with the components given by the coordinate system.

- The angle results from the ratio of generated area and maximal area
  `\angle(\mathbf{v_1},\mathbf{v_2})=\arcsin\frac{|\mathbf{v_1}\times \mathbf{v_2}|}{|\mathbf{v_1}||\mathbf{v_2}|}` 
  or from the ratio of the addable components to the whole length
  `\angle(\mathbf{v_1},\mathbf{v_2})=\arccos\frac{\mathbf{v_1}\mathbf{v_2}}{|\mathbf{v_1}||\mathbf{v_2}|}` 

  The angle between orthogonal variables is `\frac{\pi}{2}`.

- and with complex numbers
  `\angle(z_1,z_2)=\arg(\frac{z_1\bar{z_2}}{|z_2||z_2|})=\arg{z_1\bar{z_2}}`.

Another word for angle is phase, that allows to overcome the meaning of direction by common use.
Essential is the comparison of two quantities regarding the addable components.
To this end variables that do not represent a direction, but have influence on addability,
can be mapped to the angle range `[0,2\pi]`, which then is called phase.
Examples: 

- The time `t` of a vibration becomes `\varphi=\frac{2\pi}{T}t` or 
  
- the combined time and space position of a wave becomes `\varphi=\frac{2\pi}{\lambda}x+\frac{2\pi}{T}t`. 

`Ae^{i\varphi}` then represents the currently addable amplitude.

