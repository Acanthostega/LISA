# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from .canvas import Canvas
from LISA.gui.widget.axes import Axes


numpymodule.NumpyHandler.ERROR_ON_COPY = True

__all__ = ["Figure"]


class Figure(object):
    def __init__(self, name="Figure {id:d}"):
        # set the window which will be the scene
        self.canvas = Canvas("")
        self.canvas.name = name.format(id=self.canvas.id)

    def add_axes(self, nx, ny, position):
        """
        Add an axes into the figure, on which to draw objects.
        """
        # create a new axes widget
        axes = Axes(self.canvas)

        self.canvas.makeCurrent()
        axes.createShaders()

        # add the axes into the grid of the canvas
        self.canvas.grid.addWidget(axes, nx, ny, position)

        # add also the axes into the list
        self.axes.append(axes)

        return axes

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

    def addWidget(self, wid):
        self.canvas.makeCurrent()
        wid.parent = self.canvas
        self.canvas.addWidget(wid)
        wid.createShaders()

    def __getitem__(self, ind):
        return self.canvas.axes[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self.canvas.axes

    @axes.setter
    def axes(self, value):
        # create shaders if there is one
        self.canvas.makeCurrent()

        # create shaders after all is done
        value.createShaders(self.canvas)

        # store the instance for plots
        self.canvas.axes.append(value)

    def close(self):
        self.canvas.close()


# vim: set tw=79 :
