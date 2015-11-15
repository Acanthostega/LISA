#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

__all__ = [
    "Buffer",
]


class Buffer(object):
    """
    A class to manage the creation and manipulation of buffer in OpenGL.
    """
    def create(self):
        raise NotImplementedError("This essential method must be implemented!")

    def bind(self):
        raise NotImplementedError("This essential method must be implemented!")

    def release(self):
        raise NotImplementedError("This essential method must be implemented!")

    def delete(self):
        raise NotImplementedError("This essential method must be implemented!")

    @contextmanager
    def activate(self):
        """
        Used to make the bind and release changes with a simple context
        manager.
        """
        # bind the buffer
        self.bind()

        yield

        # indicate that the buffer can be released
        self.release()


# vim: set tw=79 :
