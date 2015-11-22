#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.Matrice as m
import numpy as np

from OpenGL import GL
from .matrices import Perspective
from .matrices import Orthographic


class Camera(object):
    """
    A class for managing cameras for various scenes. They handle the view, the
    projection that can be changed by the user.
    """
    def __init__(self):
        """
        Init the camera with some default projection and views.
        """
        # Different matrix use for the on screen printing:
        self._view = m.Identity()
        self._projection = Perspective(shape=(4, 4), dtype="float32")
        self._up = m.Vector(0., 1., 0., dtype="float32")
        self._target = m.Vector(0., 0., 0., dtype="float32")
        self._position = m.Vector(0, 0, 5., dtype="float32")
        self._zoom = 1.0
        self._set_view()

    def _set_view(self):
        self.view.setToIdentity()
        self.view.lookAt(
            self.position,
            self.target,
            self.up,
        )

    def rotate(self, axis, angle):
        """
        Rotate the camera around the given axis with the given angle.
        """
        # de-project the rotation axis
        rotation_axis = m.Vector(
            *(np.dot(np.linalg.inv(self.projection[:3, :3]), axis)).tolist()
        )

        # the matrix for the transformation
        rotate = m.Quaternion(
            angle,
            rotation_axis
        )
        rotate = rotate[:3, :3]

        # translate the position to the referential of the target
        moved = self.position - self.target
        moved = np.dot(rotate.T, moved)

        # put the position again in the coordinates of the world
        self.position = m.Vector(*(moved + self.target).tolist(),
                                 dtype=self.position.dtype)

    def field(self, width, height):
        GL.glViewport(0, 0, width, height)
        self.projection.ratio = width / height

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        self._view = view

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, projection):
        self._projection = projection

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self._set_view()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target
        self._set_view()

    @property
    def up(self):
        return self._up

    @up.setter
    def up(self, up):
        self._up = up
        self._set_view()

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom
        self.position = m.Vector(
            *((
                1 - self._zoom
            ) * self.target + self._zoom * self.position).tolist()
        )

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen = screen
        w, h = self._screen
        h = 1 if h == 0 else h
        self.field(w, h)

    def __repr__(self):
        """
        Show informations about the camera.
        """
        return "Camera(position={0}, target={1}, up={2},".format(
            self.position,
            self.target,
            self.up,
        ) + " projection={0}, view={1})".format(self.projection, self.view)


class TopCamera(Camera):
    """
    Camera to see the scene from the top of a 2D plane.
    """
    def __init__(self):
        # init the camera as usual
        super(TopCamera, self).__init__()

        # change z of the camera for distinction
        self._position = m.Vector(0, 0, 1., dtype="float32")

        # projection matrix used for widget
        self.projection = Orthographic(shape=(4, 4), dtype="float32")

    def field(self, width, height):
        GL.glViewport(0, 0, width, height)
        self.projection.top = 0.
        self.projection.bottom = height
        self.projection.left = 0.
        self.projection.right = width


# vim: set tw=79 :
