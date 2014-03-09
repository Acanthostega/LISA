#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys
import numpy as np
import OGLWidget as og
import Figure as f

from PyQt5 import Qt
from PyQt5 import QtGui as qg
from OpenGL import GL


class TestOGL(object):

    def __init__(self, *args, **kwargs):
        rand = np.random.rand(1000, 3)
        self._color = np.random.rand(1000, 3)

        r = rand[:, 0] ** (1. / 3.)
        thet = np.arccos(2 * rand[:, 1] - 1)
        phi = 2. * np.pi * rand[:, 2]

        self._pos = np.array(
            [
                r * np.cos(phi) * np.sin(thet),
                r * np.sin(phi) * np.sin(thet),
                r * np.cos(thet)
            ]
        ).T

        # buffer objects
        self._m_vertices = qg.QOpenGLBuffer(qg.QOpenGLBuffer.VertexBuffer)
        self._m_colors = qg.QOpenGLBuffer(qg.QOpenGLBuffer.VertexBuffer)

        # bind buffer objects
        self._m_vertices.create()
        self._m_colors.create()
        self._m_vertices.bind()
        self._m_colors.bind()

        # allocate
        self._m_vertices.allocate(self._pos.data, len(self._pos))
        self._m_colors.allocate(self._color.data, len(self._color))

        # let buffer
        self._m_vertices.release()
        self._m_colors.release()

    def show(self, shaders, matrice):
        shaders.setUniformValue("modelview", matrice)

        self._m_vertices.bind()
        shaders.setAttributeArray("in_Vertex", self._pos)
        shaders.enableAttributeArray("in_Vertex")
        self._m_vertices.release()

        self._m_colors.bind()
        shaders.setAttributeArray("in_Color", self._color)
        shaders.enableAttributeArray("in_Color")
        self._m_colors.release()

        GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0])

        shaders.disableAttributeArray("in_Vertex")
        shaders.disableAttributeArray("in_Color")

    def createWidget(self, title="Dialogue de test.", parent=None):
        dialog = Qt.QDialog(parent=parent)
        dialog.setWindowOpacity(0.4)
        dialog.setWindowTitle(title)
        dialog.setLayout(Qt.QVBoxLayout())
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        but = Qt.QPushButton()
        but.setText("Un bouton !")
        but.clicked.connect(self._push_button)
        dialog.layout().addWidget(but)

        return dialog

    def _push_button(self):
        pass


def testOGLWidget():
    app = Qt.QApplication(sys.argv)

    aff = og.OGLWidget()
    for i in range(3):
        aff.lines = TestOGL()
    aff.show()

    return app.exec_()


def testFigure():
    app = Qt.QApplication(sys.argv)

    fig = f.Figure()
    fig.axes = TestOGL()
    fig.show()

    return app.exec_()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    fig = f.Figure()
    fig.axes = TestOGL()
    fig.show()

    sys.exit(app.exec_())
