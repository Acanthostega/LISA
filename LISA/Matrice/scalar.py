#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL

__all__ = ["Boolean"]


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def _setUniformValue(self, id, GL_ns):
        GL.glUniform1i(id, self.value)


# vim: set tw=79 :
