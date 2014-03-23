#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np
import sip
import sys
import datetime

#from PyQt5.QtGui import *
from PyQt4.QtOpenGL import QGLShaderProgram as QOpenGLShaderProgram
from PyQt4.QtOpenGL import QGLBuffer as QOpenGLBuffer
from PyQt4.QtOpenGL import QGLShader as QOpenGLShader
from OpenGL import GL
from OpenGL.arrays import numpymodule
from scipy.misc import imread

import LISA.common as c

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class HeightMap(object):

    def __init__(self, *args, **kwargs):

        # create mesh
        self.npoints = 80
        X = np.linspace(-1, 1, self.npoints)
        Y = np.linspace(-1, 1, self.npoints)
        Z = np.zeros(self.npoints, dtype=np.float64)
        x, y, z = np.meshgrid(X, Y, Z)
        self._mesh = np.array([x, y, z], dtype=np.float64).T.flatten()

        # create the indices for triangles
        self._indices = np.empty(
            (self.npoints - 1, self.npoints - 1, 6),
            dtype=np.uint32
        )
        indices = np.array(range(self.npoints - 1), dtype=np.uint32)
        for i in range(self.npoints - 1):
            self._indices[i, :, 0] = indices[:] + i * self.npoints
            self._indices[i, :, 1] = indices[:] + 1 + i * self.npoints
            self._indices[i, :, 2] = indices[:] + (i + 1) * self.npoints
            self._indices[i, :, 3] = indices[:] + (i + 1) * self.npoints
            self._indices[i, :, 4] = indices[:] + 1 + (i + 1) * self.npoints
            self._indices[i, :, 5] = indices[:] + 1 + i * self.npoints
        self._indices = self._indices.flatten()

        self._time = datetime.datetime.now()

    def createShaders(self, parent):

        self._shaders = QOpenGLShaderProgram(parent)

        self._shaders.removeAllShaders()
        self._shaders.addShaderFromSourceFile(
            QOpenGLShader.Vertex,
            c.os.path.join(
                c.SHADERS_DIR,
                "heightmap/heightmap.vsh"
            )
        )
        self._shaders.addShaderFromSourceFile(
            QOpenGLShader.Fragment,
            c.os.path.join(
                c.SHADERS_DIR,
                "heightmap/heightmap.fsh"
            )
        )

        self._texture = GL.glGenTextures(1)
        im = imread(
            c.os.path.join(
                c.TEXTURE_DIR,
                "heightmap/two.png"
            )
        )
        im.astype(np.int8)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_MIN_FILTER,
            GL.GL_LINEAR,
        )
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_MAG_FILTER,
            GL.GL_LINEAR,
        )
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_WRAP_S,
            GL.GL_CLAMP,
        )
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D,
            GL.GL_TEXTURE_WRAP_T,
            GL.GL_CLAMP,
        )
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            3,
            im.shape[0],
            im.shape[1],
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            im,
        )

        if not self._shaders.link():
            raise ShadersNotLinked(
                "Linking shaders in OGLWidget.initialiseGL has failed! " +
                self._shaders.log()
            )
            sys.exit(1)

        # create buffers
        self._vertices = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._index = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self._vertices.create()
        self._index.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            sip.voidptr(self._mesh.ctypes.data),
            len(self._mesh) * 8
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            sip.voidptr(self._indices.ctypes.data),
            len(self._indices) * 4
        )
        self._index.release()

    def show(self, parent):
        self._shaders.bind()
        self._shaders.setUniformValue(
            "modelview",
            parent._projection * parent._view * parent._model
        )

        self._vertices.bind()
        self._shaders.enableAttributeArray("in_Vertex")
        self._shaders.setAttributeBuffer(
            "in_Vertex",
            GL.GL_DOUBLE,
            0,
            3
        )
        self._vertices.release()

        self._index.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            6 * (self.npoints - 1) ** 2,
            GL.GL_UNSIGNED_INT,
            None
        )
        self._index.release()

        self._shaders.disableAttributeArray("in_Vertex")
        self._shaders.release()

# vim: set tw=79 :