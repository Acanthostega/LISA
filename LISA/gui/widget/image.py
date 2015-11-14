#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.tools as t

from OpenGL import GL
from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER, Texture
from .widget import Widget


class Image(Widget):
    def __init__(self, image=None, fbo=None):
        # init parent
        super(Image, self).__init__()

        # register the image name
        self._image = image

        # and the fbo if selected
        self.fbo = fbo

        # set the size hint
        self.size_hint_x = 1
        self.size_hint_y = 1

        # default padding and margin
        self.padding = 0
        self.margin = 0

    def createShaders(self, world):
        self.world = world
        # set shaders
        self._shaders += t.shader_path("image/image.vsh")
        self._shaders += t.shader_path("image/image.fsh")

        # create buffers
        self._vertices = VBO(VERTEX_BUFFER)
        self._index = VBO(INDEX_BUFFER)
        self._vao = VAO()

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

        # window
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

    def paintEvent(self, event):
        self.image = self._image
        self._image_texture.load()
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "modelview",
            self.world._widget_projection * self._model
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
            "tex",
            self._shaders.textures.textures[0],
        )
        self._shaders.textures.activate()

        self._vao.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )

        self._vao.release()
        self._shaders.textures.release()
        self._shaders.release()

    def mouseEvent(self, event):
        pass

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        if self._image is None:
            return
        self._image_texture = Texture.fromImage(self._image)
        self._image_texture.parameters = {
            "TEXTURE_MIN_FILTER": "LINEAR",
            "TEXTURE_MAG_FILTER": "LINEAR",
            "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
            "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
        }

        #  self.width, self.height = texture.width, texture.height
        self._shaders.textures << self._image_texture

    @property
    def fbo(self):
        return self._fbo

    @fbo.setter
    def fbo(self, fbo):
        self._fbo = fbo
        if self._fbo is None:
            return

        self._image_texture = self._fbo.colorBuffers[0]

        #  self.width, self.height = texture.width, texture.height
        self._shaders.textures << self._image_texture


# vim: set tw=79 :
