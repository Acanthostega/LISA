#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys
import numpy as np
import OGLWidget as og
import Figure as f
import sip

from PyQt5 import Qt
from PyQt5 import QtGui as qg
from OpenGL import GL


class TestOGL(object):

    def __init__(self, *args, **kwargs):

        rand = np.random.rand(10000, 3)

        self._color = np.asarray(np.random.rand(10000, 3), dtype=np.float32)

        r = 1 * rand[:, 0] ** (1. / 3.)
        thet = np.arccos(2 * rand[:, 1] - 1)
        phi = 2. * np.pi * rand[:, 2]

        self._pos = np.array(
            [
                r * np.cos(phi) * np.sin(thet),
                r * np.sin(phi) * np.sin(thet),
                r * np.cos(thet),
                self._color[:, 0],
                self._color[:, 1],
                self._color[:, 2],
            ],
            dtype=np.float32,
        ).T.flatten()

        # buffer objects
        self._m_vertices = qg.QOpenGLBuffer(qg.QOpenGLBuffer.VertexBuffer)

        # bind buffer objects
        self._m_vertices.create()
        self._m_vertices.bind()

        # allocate
        self._m_vertices.allocate(
            sip.voidptr(self._pos.ctypes.data),
            len(self._pos) * 4
        )

        # let buffer
        self._m_vertices.release()

    def show(self, shaders, matrice):

        shaders.setUniformValue("modelview", matrice)

        self._m_vertices.bind()
        shaders.enableAttributeArray("in_Vertex")
        shaders.setAttributeBuffer("in_Vertex", GL.GL_FLOAT, 0, 3, 24)

        shaders.enableAttributeArray("in_Color")
        shaders.setAttributeBuffer("in_Color", GL.GL_FLOAT, 12, 3, 24)
        self._m_vertices.release()

        GL.glDrawArrays(GL.GL_POINTS, 0, len(self._pos) // 6)

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
