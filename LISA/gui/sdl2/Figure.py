# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from .events import SDLInput
from threading import Thread, Lock

import sdl2 as s


numpymodule.NumpyHandler.ERROR_ON_COPY = True


class SDL2_Deal(object):
    def __init__(self, fps=30):
        s.SDL_Init(s.SDL_INIT_VIDEO)

        self._windowList = dict()
        self._ev = SDLInput()
        self._hook = None
        self._framerate = int(1000 / fps)
        self._in_event_loop = False
        self._running = True

        # used to lock manually threads when accessing to a shared variable
        self._windows_lock = Lock()

        # create thread with the event loop
        self._create_thread()

        # launch the thread with the event loop
        self.launch_events()

    def _create_thread(self):
        """
        Create the thread object to launch the event loop.
        """
        if not self._in_event_loop:
            self._events_thread = Thread(
                target=self._dealEvents,
            )

    def launch_events(self):
        """
        If the event loop isn't already launched, launch it.
        """
        if not self._in_event_loop:
            self._in_event_loop = True
            self._events_thread.start()

    def _dealEvents(self):
        try:
            # while not stdin_ready():
            while self._running:
                start = s.SDL_GetTicks()

                self._ev.update()

                try:
                    self._windows_lock.acquire(timeout=1)
                    for win in self._windowList.values():
                        win.events(self._ev)
                        win.draw()
                finally:
                    self._windows_lock.release()

                stop = s.SDL_GetTicks()
                duree = (stop - start)
                if duree < self._framerate:
                    s.SDL_Delay(self._framerate - duree)
        except Exception as e:
            print(e)

    def add(self, val):
        with self._windows_lock:
            self._windowList[val.id] = val

    def erase(self, val):
        del self._windowList[val.id]

    def __del__(self):
        """
        Clean delete of all variables.
        """

        print("Coucou")
        # kill the thread
        self._running = False
        self._windows_lock.release()

        # quit SQL
        s.SDL_Quit()

_ipython_way_sdl2 = SDL2_Deal()


from .OGLWidget import OGLWidget


class Figure(object):

    def __init__(self, *args, **kwargs):

        # set the window which will be the scene
        self.scene = OGLWidget("Hello world")

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

    def addWidget(self, wid):
        pass

    def resizeEvent(self, event):
        if self.scene:
            self.scene.resizeGL(event.size().width(), event.size().height())
            super(Figure, self).resizeEvent(event)

    def __getitem__(self, ind):
        return self.scene.lines[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self.scene.lines

    @axes.setter
    def axes(self, value):

        # create shaders if there is one
        self.scene.makeCurrent()
        try:
            value.createShaders(self.scene)
        except AttributeError as e:
            print(e)

        # add widget created by user
        try:
            wid = value.createWidget()
            if wid:
                self.addWidget(wid)
        except:
            pass

        # store the instance for plots
        self.scene.lines = value

    def close(self):
        self.scene.close()
