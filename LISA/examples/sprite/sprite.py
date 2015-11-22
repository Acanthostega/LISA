#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL
from OpenGL.arrays import numpymodule

import LISA.tools as t
import LISA.Object as o

from LISA.Matrice import Vector
from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class Sprites(o.Base):
    def __init__(self, *args, **kwargs):

        npoints = 10000
        rand = np.random.rand(npoints, 3)

        r = rand[:, 0] ** (1. / 3.)
        thet = np.arccos(2 * rand[:, 1] - 1)
        phi = 2. * np.pi * rand[:, 2]

        pos = np.array(
            [
                r * np.cos(phi) * np.sin(thet),
                r * np.sin(phi) * np.sin(thet),
                r * np.cos(thet)
            ],
            dtype=np.float32,
        ).T

        self._indices = np.array(range(npoints)).astype("uint32")

        super(Sprites, self).__init__(pos)

        self._shaders += t.shader_path("sprite/sprite.vsh")
        self._shaders += t.shader_path("sprite/sprite.fsh")

        # create buffers
        self._vertices = VBO("Sprites vertices", VERTEX_BUFFER)
        self._index = VBO("Sprites indexes", INDEX_BUFFER)
        self._vao = VAO("Sprites")

    def createShaders(self):
        self._vertices.create()
        self._index.create()
        self._vao.create()

        # allocate buffers
        with self._vertices.activate():
            self._vertices.allocate(
                self._data,
                len(self._data) * 4
            )

        with self._index.activate():
            self._index.allocate(
                self._indices,
                len(self._indices) * 4
            )

        self._shaders.build()
        self._shaders.bindAttribLocation("position")
        self._shaders.link()

        with self._vao.activate():
            self._vertices.bind()
            self._shaders.enableAttributeArray("position")
            self._shaders.setAttributeBuffer(
                "position",
                self._data,
            )

            self._index.bind()

    def paintEvent(self, event):
        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_FALSE)

        matrice = event.world.camera.view * self._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue(
            "projection",
            event.world.camera.projection,
        )
        self._shaders.setUniformValue("screenSize", event.world.screensize)
        self._shaders.setUniformValue("voxelSize", Vector(0.01))

        with self._vao.activate():
            GL.glDrawElements(
                GL.GL_POINTS,
                self._data.shape[0] // 3,
                GL.GL_UNSIGNED_INT,
                None,
            )

        self._shaders.release()

        GL.glDisable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)


# vim: set tw=79 :
