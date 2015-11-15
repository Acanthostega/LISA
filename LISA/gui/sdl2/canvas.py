# -*- coding:Utf8 -*-

import logging
import LISA.Matrice as m

from OpenGL.arrays import numpymodule
from OpenGL import GL

from LISA.gui.utils.cameras import TopCamera
from LISA.gui.utils.cameras import Camera
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

        # set the top view camera
        self.camera = Camera()
        self.camera.screen = self.screensize
        self.widget_camera = TopCamera()
        self.widget_camera.screen = self.screensize

    def addWidget(self, widget):
        if hasattr(widget, "paintEvent"):
            widget.world = self
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
        self.camera.screen = event.size
        self.widget_camera.screen = event.size
        self.update()

    def paintEvent(self, event):
        self.makeCurrent()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for axe in self.axes:
            axe.paintEvent(event)

        # now loop over widgets
        for widget in self.widgets:
            widget.paintEvent(event)

        self.swap()

    def mousePressEvent(self, event):
        super(Canvas, self).mousePressEvent(event)
        if event.accepted:
            return
        # say the mouse is pressed
        self._mousePress = True

    def mouseReleaseEvent(self, event):
        super(Canvas, self).mouseReleaseEvent(event)
        self._mousePress = False

    def mouseMoveEvent(self, event):
        super(Canvas, self).mouseMoveEvent(event)
        if event.accepted:
            return

        if self._mousePress:
            # compute the movement of the mouse
            x, y = event.dx, event.dy

            # if no movement, do nothing
            if x == 0 and y == 0:
                return

            # create the rotation axis
            rotationAxis = m.Vector(y, x, 0.0)

            # make the angular speed to its norm
            angularSpeed = rotationAxis.norm()

            # move the camera
            self.camera.rotate(rotationAxis, angularSpeed)

            # refresh
            self.update()

    def wheelEvent(self, event):
        super(Canvas, self).wheelEvent(event)

        delta = event.dy

        if delta < 0:
            self.camera.zoom = 1.15
        elif delta > 0:
            self.camera.zoom = 0.87

        self.update()

    def showEvent(self, event):
        self.update()

    def exposeEvent(self, event):
        self.update()


# vim: set tw=79 :
