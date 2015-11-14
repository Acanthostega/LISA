#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes

from OpenGL import GL
from scipy.misc import imread

from LISA.Matrice import Vector
from LISA.tools import DTYPE_TO_GL
from LISA.tools.metaclasses import SingletonManager

__all__ = ["Texture"]


class Texture(metaclass=SingletonManager):
    """
    A class representation of a texture.
    """
    def __init__(self, name, **kwargs):
        self.name = name

        # loop over keyword arguments
        for k, v in kwargs.items():
            setattr(self, k, v)

        self._binded = False
        self._loaded = False
        self.deep = None
        self.level = 0
        self.unit = 0
        self.id = GL.glGenTextures(1)

    def bind(self):
        if not self._binded:
            GL.glBindTexture(
                self._kind,
                self.id,
            )
            self._binded = True

    def release(self):
        """
        To indicate that the texture should not be used anymore.
        """
        if self._binded:
            GL.glBindTexture(
                self._kind,
                0,
            )
            self._binded = False

    def setParameter(self, param, value):
        GLvalue = self._getValue(value)
        func = self._getTexParameter(GLvalue)
        self.bind()
        func(
            self._kind,
            self._getParameter(param),
            GLvalue,
        )

    def _getTexParameter(self, value):
        func = None
        if isinstance(value, float):
            func = GL.glTexParameterf
        elif isinstance(value, int):
            func = GL.glTexParameteri
        elif isinstance(value, Vector):
            if "float" in value.dtype.name:
                func = GL.glTexParameterfv
            elif "int" in value.dtype.name:
                func = GL.glTexParameteriv
        if not func:
            raise ValueError(
                "The passed value isn't already managed <<{0}>>".format(
                    type(value)
                )
            )
        return func

    def _getParameter(self, param):
        parameter = "GL_" + param.upper()
        if hasattr(GL, parameter):
            return getattr(GL, parameter)
        raise AttributeError(
            "The parameter {0} doesn't exist in OpenGL!".format(parameter)
        )

    def _getValue(self, value):
        if isinstance(value, str):
            parameter = "GL_" + value.upper()
            if hasattr(GL, parameter):
                return getattr(GL, parameter)
            raise AttributeError(
                "The value {0} doesn't exist in OpenGL!".format(parameter)
            )
        return value

    def load(self):
        """
        Load the texture into memory with the parameters specified in the
        properties of the texture instance.
        """
        if self._loaded:
            return

        # bind the texture to the opengl context
        self.bind()

        # create the list of values since it can be variable
        values = [
            self._kind,
            self.level,
            self.format,
            self.width,
            self.height,
            0,
            self.format,
            self.type,
            self.data,
        ]

        # say opengl where is the data for the texture
        self._teximage(*[x for x in values])

        self._loaded = True

    def activate(self):
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.unit)
        self.bind()

    def _setUniformValue(self, location, GL_ns):
        GL_ns["glUniform1i"](location, self.unit)

    @classmethod
    def fromImage(cls, filename, dtype="uint8", format="RGBA", **kwargs):
        """
        Create a texture from an image file.
        """
        # create the texture
        texture = cls(filename, **kwargs)

        # read image from file
        image = imread(filename)
        image = image.astype(dtype)
        texture.kind = "2D"
        texture.width = image.shape[1]
        texture.height = image.shape[0]
        texture.type = DTYPE_TO_GL[image.dtype.name]
        texture.data = image
        texture.format = format

        return texture

    @classmethod
    def fromSDLSurface(cls, surface, **kwargs):
        """
        Create a texture from a SDL surface.
        """
        # create the texture
        texture = cls(id(surface), **kwargs)
        texture.kind = "2D"
        texture.width = surface.w
        texture.height = surface.h
        texture.type = GL.GL_UNSIGNED_BYTE
        texture.data = ctypes.c_void_p(surface.pixels)
        texture.format = "RGBA"

        return texture

    def delete(self):
        """
        Remove the texture from the manager and delete the texture from the
        GPU.
        """
        # remove from the manager
        self.manager.delete(self)

        # remove from the GPU
        GL.glDeleteTextures([self.id])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def kind(self):
        return self._kind_name

    @kind.setter
    def kind(self, kind):
        self._kind_name = kind.upper()
        self._kind = getattr(GL, "GL_TEXTURE_" + self._kind_name)
        self._teximage = getattr(GL, "glTexImage" + self._kind_name)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters
        for key, value in self._parameters.items():
            self.setParameter(key, value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def deep(self):
        return self._deep

    @deep.setter
    def deep(self, deep):
        self._deep = deep

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format):
        self._format = getattr(GL, "GL_" + format)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


# vim: set tw=79 :
