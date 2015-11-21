#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.tools as t
import LISA.Matrice as m

from OpenGL import GL
from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.OpenGL import Shaders
from LISA.Matrice import Vector


class Widget(object):
    def __init__(self):

        # the mesh used to draw the widget on the screen
        self._mesh = np.array(
            [0., 0., 0.0,
             0., 1, 0.0,
             1, 1, 0.0,
             1, 0, 0.0],
            dtype=np.float32,
        )
        self._indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        self._npoints = len(self._indices)

        # the upper left corner of the widget
        self._corner = Vector(0, 0, dtype=np.float32)

        # the size of the widget
        self._size = Vector(1., 1., dtype=np.float32)
        self._minWidth, self._minHeight = 0., 0.

        # for borders
        self._borders = [10, 10]

        # for events
        self._mousePress = False
        self._mousePressBorders = False
        self._mouse = Vector(0., 0., dtype=np.float32)
        self._mouseOffset = Vector(0., 0., dtype=np.float32)

        # init shaders
        self._shaders = Shaders()

        # the matrix model
        self._model = m.Identity()

        # a list of children object
        self._children = []

        # set default padding and margin for the widget
        self.padding = 5
        self.margin = 3

        # set the size_hint
        self.size_hint = None

        # set the parent
        self._parent = None

        # set the default color
        self.bgcolor = 0.1, 0.1, 0.1, 0.7

    def addWidget(self, widget):
        """
        Add a widget in the list of children and set correctly sizes
        accordingly to the parent.
        """

        # set the parent of the widget
        widget.parent = self

        # append the widget to children
        self._children.append(widget)

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        self._world = world

    @property
    def bgcolor(self):
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, color):
        self._bgcolor = Vector(*color, dtype=np.float32)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def minWidth(self):
        return self._minWidth

    @minWidth.setter
    def minWidth(self, minWidth):
        self._minWidth = minWidth
        if self.parent is not None:
            self.parent.minWidth = float(self._minWidth + self.margin_x.sum())
        if self.width < self._minWidth:
            self.width = self._minWidth

    @property
    def minHeight(self):
        return self._minHeight

    @minHeight.setter
    def minHeight(self, minHeight):
        self._minHeight = minHeight
        if self.parent is not None:
            self.parent.minHeight = float(
                self._minHeight + self.margin_y.sum()
            )
        if self.height < self._minHeight:
            self.height = self._minHeight

    @property
    def x_border(self):
        return self._x_border

    @x_border.setter
    def x_border(self, x_border):
        self._x_border = x_border
        self._border[0] = self._x_border

    @property
    def y_border(self):
        return self._y_border

    @y_border.setter
    def y_border(self, y_border):
        self._y_border = y_border
        self._border[1] = self._y_border

    @property
    def width(self):
        return self._size[0]

    @width.setter
    def width(self, width):
        self._size[0] = width
        if self._size[0] <= self.minWidth:
            self._size[0] = self.minWidth
        #  if self.parent is not None:
            #  self.parent.width = self._size[0]

    @property
    def height(self):
        return self._size[1]

    @height.setter
    def height(self, height):
        self._size[1] = height
        if self._size[1] < self.minHeight:
            self._size[1] = self.minHeight
        #  if self.parent is not None:
            #  self.parent.height = self._size[1]

    @property
    def x(self):
        return self._corner[0]

    @x.setter
    def x(self, x):
        self._corner[0] = x

    @property
    def y(self):
        return self._corner[1]

    @y.setter
    def y(self, y):
        self._corner[1] = y

    @property
    def size_hint(self):
        return self._size_hint

    @size_hint.setter
    def size_hint(self, size_hint):
        self._size_hint = [size_hint] * 2

    @property
    def size_hint_x(self):
        return self._size_hint[0]

    @size_hint_x.setter
    def size_hint_x(self, size_hint_x):
        self._size_hint[0] = size_hint_x

    @property
    def size_hint_y(self):
        return self._size_hint[1]

    @size_hint_y.setter
    def size_hint_y(self, size_hint_y):
        self._size_hint[1] = size_hint_y

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = Vector(*[padding] * 4, dtype=np.float32)

    @property
    def padding_x(self):
        return self._padding[:2]

    @padding_x.setter
    def padding_x(self, padding_x):
        self._padding[:2] = padding_x

    @property
    def padding_y(self):
        return self._padding[2:]

    @padding_y.setter
    def padding_y(self, padding_y):
        self._padding[2:] = padding_y

    @property
    def padding_left(self):
        return self._padding[0]

    @padding_left.setter
    def padding_left(self, padding_left):
        self._padding[0] = padding_left

    @property
    def padding_right(self):
        return self._padding[1]

    @padding_right.setter
    def padding_right(self, padding_right):
        self._padding[1] = padding_right

    @property
    def padding_top(self):
        return self._padding[2]

    @padding_top.setter
    def padding_top(self, padding_top):
        self._padding[2] = padding_top

    @property
    def padding_bottom(self):
        return self._padding[3]

    @padding_bottom.setter
    def padding_bottom(self, padding_bottom):
        self._padding[3] = padding_bottom

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin):
        self._margin = Vector(*[margin] * 4, dtype=np.float32)

    @property
    def margin_x(self):
        return self._margin[:2]

    @margin_x.setter
    def margin_x(self, margin_x):
        self._margin[:2] = margin_x

    @property
    def margin_y(self):
        return self._margin[2:]

    @margin_y.setter
    def margin_y(self, margin_y):
        self._margin[2:] = margin_y

    @property
    def margin_left(self):
        return self._margin[0]

    @margin_left.setter
    def margin_left(self, margin_left):
        self._margin[0] = margin_left

    @property
    def margin_right(self):
        return self._margin[1]

    @margin_right.setter
    def margin_right(self, margin_right):
        self._margin[1] = margin_right

    @property
    def margin_top(self):
        return self._margin[2]

    @margin_top.setter
    def margin_top(self, margin_top):
        self._margin[2] = margin_top

    @property
    def margin_bottom(self):
        return self._margin[3]

    @margin_bottom.setter
    def margin_bottom(self, margin_bottom):
        self._margin[3] = margin_bottom

    def createShaders(self, world):
        self.world = world

        self._shaders += t.shader_path("widget/widget.vsh")
        self._shaders += t.shader_path("widget/widget.fsh")

        # create buffers
        self._vertices = VBO("Widget square", VERTEX_BUFFER)
        self._index = VBO("Widget square indexes", INDEX_BUFFER)
        self._vao = VAO("Widget")

        self._vertices.create()
        self._index.create()
        self._vao.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._mesh,
            len(self._mesh) * 4
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            self._indices,
            len(self._indices) * 4
        )
        self._index.release()

        self._shaders.build()
        self._shaders.bindAttribLocation("window")
        self._shaders.link()

        self._vao.bind()

        self._vertices.bind()
        self._shaders.enableAttributeArray("window")
        self._shaders.setAttributeBuffer(
            "window",
            self._mesh,
        )
        self._index.bind()

        self._vao.release()

        for widget in self._children:
            widget.createShaders(world)

    def paintEvent(self, event):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "modelview",
            self.world.widget_camera.projection * self._model
        )

        self._shaders.setUniformValue(
            "corner",
            self._corner,
        )
        self._shaders.setUniformValue(
            "size",
            self._size,
        )
        self._shaders.setUniformValue(
            "color",
            self._bgcolor,
        )

        self._vao.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )

        self._vao.release()
        self._shaders.release()

        for widget in self._children:
            widget.paintEvent(event)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        for widget in self._children:
            widget.keyReleaseEvent(event)
            if event.accepted:
                break

    def keyPressEvent(self, event):
        for widget in self._children:
            widget.keyPressEvent(event)
            if event.accepted:
                break

    def wheelEvent(self, event):
        for widget in self._children:
            widget.wheelEvent(event)
            if event.accepted:
                break

    def closeEvent(self, event):
        pass

    def resizeEvent(self, event):
        pass

    def inside(self, x, y):
        """
        Method returning true if the widget accepts the events because the
        mouse is over it, else returns false.
        """
        return (
            self._corner[0] <= x <= self._corner[0] + self._size[0]
            and
            self._corner[1] <= y <= self._corner[1] + self._size[1]
        )

    def _inside_border(self, x, y):
        return (
            self._corner[0] + self._size[0] - self._borders[0] <=
            x <= self._corner[0] + self._size[0] and
            self._corner[1] + self._size[1] - self._borders[1] <=
            y <= self._corner[1] + self._size[1]
        )

    def update(self):
        self.parent.update()


# vim: set tw=79 :
