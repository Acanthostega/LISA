# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from .canvas import Canvas


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
    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

    def addWidget(self, wid):
        wid.parent = self.canvas
        self.canvas.addWidget(wid)

    def __getitem__(self, ind):
        return self.scene.lines[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self.scene.lines

    @axes.setter
    def axes(self, value):
        # create shaders if there is one
        self.canvas.makeCurrent()

        # add widget created by user
        if hasattr(value, "createWidget"):
            wid = value.createWidget()
            if wid:
                self.addWidget(wid)
            # create shaders for widget
            wid.createShaders(self.canvas)

        # create shaders after all is done
        value.createShaders(self.canvas)

        # store the instance for plots
        self.canvas.axes.append(value)

    def close(self):
        self.scene.close()


# vim: set tw=79 :
