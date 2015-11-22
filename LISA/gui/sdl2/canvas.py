# -*- coding:Utf8 -*-

import logging

from OpenGL.arrays import numpymodule
from OpenGL import GL

from LISA.gui.utils.cameras import TopCamera
from LISA.gui.widget import GridLayout
from .window import SDLWindow
from .hook import EventLoop
from .application_events import PaintEvent
from .application_events import Paint

numpymodule.NumpyHandler.ERROR_ON_COPY = True

logger = logging.getLogger(__name__)


__all__ = ["Canvas"]


class Canvas(SDLWindow):
    def __init__(self, *args, **kwargs):
        # Data class to plot:
        self.axes = []

        # widgets to draw
        self.widgets = []

        # Some variables use to keep track of what we are doing with events:
        self._mousePress = False

        # init the window as usual
        super(Canvas, self).__init__(*args, **kwargs)
        self.camera = TopCamera()
        self.camera.screen = self.screensize

        # a gridlayout for containing the axes
        self.grid = GridLayout()
        #  self.grid = VerticalLayout()
        self.grid.size_hint = 1
        self.grid.margin = 0
        self.grid.padding = 0
        self.makeCurrent()
        self.grid.createShaders()

    def addWidget(self, widget):
        if hasattr(widget, "paintEvent"):
            self.makeCurrent()
            widget.createShaders()
            self.widgets.append(widget)
        else:
            logger.error(
                "A widget must have a paintEvent method to be " +
                "displayed on the window!"
            )

    def update(self):
        """
        Send a event into the queue to redraw the window.
        """
        EventLoop.instance.postEvent(self, PaintEvent(Paint, self))

    def resizeEvent(self, event):
        super(Canvas, self).resizeEvent(event)

        # indicate new size to cameras
        self.camera.screen = event.size

        # set the new size to the grid for axes
        self.grid.width = event.size[0]
        self.grid.height = event.size[1]

        # loop oiver axes to send resize event
        for axe in self.axes:
            axe.resizeEvent(event)

        # refresh the page
        self.update()

    def mousePressEvent(self, event):
        # first send event to widgets as usual
        super(Canvas, self).mousePressEvent(event)

        # dispatch it to axes
        for axe in self.axes:
            if axe.inside(event.x, event.y):
                axe.mousePressEvent(event)
                return

    def mouseReleaseEvent(self, event):
        # first send event to widgets as usual
        super(Canvas, self).mouseReleaseEvent(event)

        # dispatch it to axes
        for axe in self.axes:
            axe.mouseReleaseEvent(event)
            if event.accepted:
                return

    def mouseMoveEvent(self, event):
        # first send event to widgets as usual
        super(Canvas, self).mouseMoveEvent(event)

        # dispatch it to axes
        for axe in self.axes:
            axe.mouseMoveEvent(event)
            if event.accepted:
                return

    def wheelEvent(self, event):
        # first send event to widgets as usual
        super(Canvas, self).wheelEvent(event)

        # dispatch it to axes
        for axe in self.axes:
            axe.wheelEvent(event)
            if event.accepted:
                return

    def paintEvent(self, event):
        self.makeCurrent()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for axe in self.axes:
            axe.paintEvent(event)

        # now loop over widgets
        for widget in self.widgets:
            widget.paintEvent(event)

        self.swap()

    def showEvent(self, event):
        self.update()

    def exposeEvent(self, event):
        self.update()


# vim: set tw=79 :
