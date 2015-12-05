#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from LISA.Matrice import Identity
from LISA.Matrice import Translation
from LISA.Matrice import Vector

__all__ = ["Scene"]


class Scene(object):
    """
    Container for scenes and objects for managing their positions inside the
    world.
    """
    def __init__(self):
        """
        The model matrix of the scene is the identity initially and it contains
        no children nodes.
        """
        # init internal tranformation
        self._model = Identity()

        # no children at start
        self.children = []

        # flag to say if we need to redraw all
        self._dirty = True

    def add(self, node):
        """
        Add a node to the scene graph.
        """
        node.canvas = self.canvas
        self.canvas.makeCurrent()
        node.createShaders()
        self.children.append(node)

    def remove(self, node):
        """
        Remove a node from the scene graph.
        """
        self.children.remove(node)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model * self._model
        self._dirty = True

    def paintEvent(self, event):
        self.render(event, self.model, self._dirty)

    def render(self, event, parent_world, dirty):
        """
        Used to render all the scene without redrawing unnecessarily if the an
        object changed in the graph.
        """
        # dirty flag to redraw or not
        dirty = dirty or self._dirty

        # compute the transformation
        if dirty:
            world = parent_world * self.model
            self._dirty

        # render child with the new transform
        for child in self.children:
            child.render(event, world, dirty)

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas):
        self._canvas = canvas

    def createShaders(self, *args):
        """
        Do nothing, just to fake an object.
        """
        pass

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.model = Translation(Vector(x, 0, 0))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.model = Translation(Vector(0, y, 0))

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z
        self.model = Translation(Vector(0, 0, z))


# vim: set tw=79 :
