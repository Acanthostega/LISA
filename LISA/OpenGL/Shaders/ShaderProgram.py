#!/usr/bin/env python
# encoding: utf-8

from OpenGL import GL


_GL_ns = vars(GL)
_TypeNP_OGL = dict(
)
_TypeNP_OGL["float64"] = GL.GL_DOUBLE
_TypeNP_OGL["float32"] = GL.GL_FLOAT


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class ShaderProgram(object):

    def __init__(self):
        self._id = GL.glCreateProgram()
        self._shaders = list()
        self._last_id = 0
        self._enableAttrib = dict()

    @property
    def id(self):
        return self._id

    def setUniformValue(self, name, data):
        var_id = GL.glGetUniformLocation(self.id, name.encode())
        data._setUniformValue(var_id, _GL_ns)

    def enableAttributeArray(self, name):
        if name not in self._enableAttrib:
            GL.glBindAttribLocation(self.id, self._last_id, name.encode())
            self._enableAttrib[name] = self._last_id
            self._last_id += 1

        GL.glEnableVertexAttribArray(
            self._enableAttrib[name]
        )

    def setAttributeArray(
        self,
        name,
        data,
        tuplesize=3,
        normalized=GL.GL_TRUE,
        offset=0,
    ):
        GL.glVertexAttribPointer(
            self._enableAttrib[name],
            tuplesize,
            _TypeNP_OGL[data.dtype.name],
            normalized,
            offset,
            data
        )

    def setAttributeBuffer(
        self,
        name,
        data,
        tuplesize=3,
        normalized=GL.GL_TRUE,
        offset=0,
    ):
        GL.glVertexAttribPointer(
            self._enableAttrib[name],
            tuplesize,
            _TypeNP_OGL[data.dtype.name],
            normalized,
            offset,
            None,
        )

    def disableAttributeArray(self, name):
        GL.glDisableVertexAttribArray(self._enableAttrib[name])

    def addShader(self, val):
        self._shaders.append(val)
        GL.glAttachShader(
            self.id,
            val.id
        )

    def removeShader(self, val):
        self._shaders.remove(val)
        GL.glDetachShader(
            self.id,
            val.id
        )

    def link(self):
        GL.glLinkProgram(self.id)

    def bind(self):
        GL.glUseProgram(self.id)

    def release(self):
        GL.glUseProgram(0)

    def __add__(self, val):
        self.addShader(val)
        return self

    def __iadd__(self, val):
        self.addShader(val)
        return self

    def __radd__(self, val):
        self.addShader(val)
        return self

    def __contains__(self, val):
        return val in self._shaders

    def __sub__(self, val):
        self.removeShader(val)
        return self

    def __isub__(self, val):
        self.removeShader(val)
        return self

    def __del__(self):
        if bool(GL.glDeleteProgram):
            GL.glDeleteProgram(self.id)