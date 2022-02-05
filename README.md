# Py_Turtle_to_img
This library is intended to allow you to translate a drawing made by turtle into an image, 
both as a pixel graphic (PNG, JPG, JPEG...) and vector graphic (SVG).

***PLEASE NOTE: THIS LIBRARY IS INTENDED FOR PRIVATE USE ONLY. THAT IS TO SAY THAT IT SUCKS. USE WITH CAUTION.***

For this library to work, you will also need to install Pillow, if you haven't already. you can simply do
so by typing
```
python -m pip install Pillow
```
into your console.


## Classes
the library includes 3 classes (PNG_Pen, SVG_Pen, Points), as well as one base class for all of them.
since they are all built for mostly the same purpose, they share most of their functions, such as:
- forward(dist)
- left(deg) / right(deg)
- goto(x, y)

and so on. These functions are all based on the turtle library for python, so you will find more
information [there.](https://docs.python.org/3/library/turtle.html)

there are some exceptions, however, that are worth mentioning:


> ### Points
> This class is not intended to draw by itself. What it does is store its position in a list everytime its position
> gets updated. `get_points()` will return this list and `flush_points()` will empty it.
>
> ### PNG_Pen
> PNG_Pen gains an extra function called `show()`, which lets you preview your image before saving. 
> It exists purely because the pillow library allowed for it. It is therefore not included in SVG_Pen.
>
> ### SVG_Pen()
> SVG_Pen has an extra function called `path()`, which takes a list of coordinates (syntax: tuple(x, y)) and 
> creates a path that follows these points. It is different from `forward()`, as the latter just creates a single line
> everytime the function is called, while the former stores all these lines as a single path. It is recommended to 
> use a `Points` object to trace your path first and then use the path coordinates given by that object to then draw
> that path.
> 
> 
>### Other
> Both the PNG_Pen and the SVG_Pen also have a function called `save(name)`, which you can use to save the resulting image.