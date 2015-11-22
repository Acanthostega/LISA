#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.Matrice as m
import LISA.tools as t

from LISA.gui.utils.cameras import Camera
from LISA.OpenGL import FBO
from .image import Image
from OpenGL import GL


class Axes(Image):
    """
    An axes derives from a widget image.
    """
    def __init__(self, canvas):
        # store reference to the canvas
        self.canvas = canvas

        # Data class to plot:
        self.axes = []

        # Some variables use to keep track of what we are doing with events:
        self._mousePress = False

        # create the fbo for the axes
        self._fbo = FBO(478, 521)

        # init the window as usual
        super(Axes, self).__init__(fbo=self.fbo)

        # set the top view camera
        self.camera = Camera()
        #  self.camera.screen = self._size
        self.camera.screen = [self._fbo.width, self._fbo.height]

    def add(self, axes):
        # make current
        self.canvas.makeCurrent()
        axes.axes = self

        axes.createShaders()

        self.axes.append(axes)

    def update(self):
        """
        Send an event into the queue to redraw the window.
        """
        self.canvas.update()

    def resizeEvent(self, event):
        # indicate new size to cameras
        #  self.camera.screen = event.size
        pass

    def paintEvent(self, event):
        # hook to force camera
        camera = event.world.camera
        event.world.camera = self.camera
        self.camera.screen = self.camera.screen

        # render content of the axes into the fbo
        with self._fbo.activate():
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            for axe in self.axes:
                axe.paintEvent(event)

        # put agin the camera of the canvas
        camera.screen = camera.screen
        event.world.camera = camera

        # render the axes in the fbp
        super(Axes, self).paintEvent(event)

    def mousePressEvent(self, event):
        super(Axes, self).mousePressEvent(event)
        if event.accepted:
            return
        # say the mouse is pressed
        self._mousePress = True

    def mouseReleaseEvent(self, event):
        super(Axes, self).mouseReleaseEvent(event)
        self._mousePress = False

    def mouseMoveEvent(self, event):
        super(Axes, self).mouseMoveEvent(event)
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
        super(Axes, self).wheelEvent(event)

        delta = event.dy

        if delta < 0:
            self.camera.zoom = 1.15
        elif delta > 0:
            self.camera.zoom = 0.87

        self.update()


# vim: set tw=79 :
