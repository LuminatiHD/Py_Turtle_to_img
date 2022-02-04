from PIL import Image, ImageDraw
from math import sin, cos, pi

template = lambda height, width: f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   sodipodi:docname="test.svg"
   inkscape:version="1.0 (4035a4fb49, 2020-05-01)"
   id="svg8"
   version="1.1"
   viewBox="0 0 {height} {width}"
   height="{height}mm"
   width="{width}mm">
  <defs
     id="defs2" />
  <sodipodi:namedview
     inkscape:window-maximized="1"
     inkscape:window-y="-9"
     inkscape:window-x="-9"
     inkscape:window-height="991"
     inkscape:window-width="1920"
     showgrid="false"
     inkscape:document-rotation="0"
     inkscape:current-layer="layer1"
     inkscape:document-units="mm"
     inkscape:cy="410.35581"
     inkscape:cx="308.04907"
     inkscape:zoom="0.98994949"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     borderopacity="1.0"
     bordercolor="#666666"
     pagecolor="#ffffff"
     id="base" />
  <metadata
     id="metadata5">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     id="layer1"
     inkscape:groupmode="layer"
     inkscape:label="Ebene 1">
  </g>
</svg>
"""

colors = {"black": "#000000", "white": "#ffffff"}


def fixcolor(color: str):
    if type(color) == int:
        color = "#" + hex(color)[2:]

    elif type(color) != str:
        color = str(color)

    color = color.lower()

    if color in colors:
        color = colors[color]

    if not color.startswith("#") or len(color) != len("#000000"):
        raise ValueError("Color not correctly written or not implemented (syntax: \"#<HEX>\")")

    else:
        try:
            int(color[1:], 16)
        except ValueError:
            raise ValueError("Color not correctly written or not implemented (syntax: \"#<HEX>\")")

    return color


class Pen():
    def __init__(self) -> None:
        self._pos = (0, 0)
        self._rot = 0
        self._pensize = 1
        self._isdrawing = True
        self._pencolor = "#000000"

    def right(self, phi):
        phi = (phi / 360) * 2 * pi
        self._rot = (self._rot + phi)

    def left(self, phi):
        phi = (phi / 360) * 2 * pi

        self._rot = (self._rot - phi)

    def setheading(self, phi):
        self._rot = (phi / 360) * 2 * pi

    def penup(self):
        self._isdrawing = False

    def pendown(self):
        self._isdrawing = True

    def heading(self):
        return (self._rot / (2 * pi) * 360)%360

    def xcor(self):
        return self._pos[0]

    def ycor(self):
        return self._pos[1]

    def pos(self):
        return self._pos

    def pencolor(self, color):
        self._pencolor = fixcolor(color)

    def pensize(self, size=None):
        if not size:
            return self._pensize
        else:
            if type(size) == int:
                self._pensize = size

            else:
                raise ValueError("Pensize must be an integer")


class PNG_Pen(Pen):
    def __init__(self, size=(1000, 1000)) -> None:
        img = Image.new("RGB", size, (255, 255, 255))
        super().__init__()
        self.__realpen = ImageDraw.Draw(img)
        self.__img = img

    def forward(self, dist, color="black"):
        newpos = (self._pos[0] + dist * sin(self._rot), self._pos[1] + dist * cos(self._rot))
        self.goto(newpos[0], newpos[1])

    def goto(self, x, y):
        if self._isdrawing:
            color = []
            for i in range(1, 7, 2):
                color.append(int(self._pencolor[i:i+2], 16))

            self.__realpen.line((self.__img.size[0] / 2 + self.xcor(), self.__img.size[1] / 2 - self.ycor(),
                                 self.__img.size[0] / 2 + x, self.__img.size[1] / 2 - y),
                                fill=tuple(color), width=self._pensize)

        self._pos = (x, y)

    def show(self):
        self.__img.show()

    def save(self, name):
        print(name)
        self.__img.save(name)


class SVG_Pen(Pen):
    def __init__(self, size: tuple = (250, 250)):
        super().__init__()
        self.__img = template(size[0], size[1])
        self.elem_amount = 0
        self.size = size
        self._pos = (0, 0)

    def forward(self, dist):
        newpos = (self._pos[0] + dist * sin(self._rot), self._pos[1] + dist * cos(self._rot))
        self.goto(newpos[0], newpos[1])

    def goto(self, x, y):
        newpos = (x + self.size[0] / 2, y + self.size[1] / 2)
        if self._isdrawing:
            path = f"""    <path\n       id="path{self.elem_amount}"\n       
            d="M {self.xcor() + self.size[0] / 2},{self.ycor() + self.size[1] / 2} {newpos[0]},{newpos[1]}"\n
            style="fill:none;stroke:{self._pencolor};stroke-width:{self._pensize}px;stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1" />\n"""

            self.__img = self.__img[:self.__img.index("</g>")] + path + self.__img[self.__img.index("</g>"):]

        self._pos = (x, y)
        self.elem_amount += 1

    def path(self, *points):
        if len(points) == 1:
            points = points[0]

        if self._isdrawing:
            path_preset = [f"""    <path\n       id="path{self.elem_amount}"\n       d="M """, f""" "\n
            style="fill:none;stroke:{self._pencolor};stroke-width:{self._pensize}px;stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1" />\n"""]
            for i in points:
                x = i[0] + self.size[0] / 2
                y = i[1] + self.size[1] / 2
                path_preset[0] += f"{x},{y} "

            self.__img = self.__img[:self.__img.index("</g>")] + path_preset[0] + path_preset[1] + self.__img[
                                                                                                   self.__img.index(
                                                                                                       "</g>"):]
            self.elem_amount += 1

        self._pos = points[-1]

    def save(self, name):
        with open(name, "w") as file:
            file.write(self.__img)


class Points(Pen):
    def __init__(self) -> None:
        super().__init__()
        self.points = []

    def forward(self, dist):
        newpos = (self._pos[0] + dist * sin(self._rot), self._pos[1] + dist * cos(self._rot))
        self._pos = newpos
        if self._isdrawing:
            self.points.append(newpos)

    def goto(self, x, y):
        self._pos = x, y
        if self._isdrawing:
            self.points.append((x, y))

