#!/usr/bin/env python

import traceback
import argparse
import logging
from LISA.gui.sdl2.Figure import Figure
from LISA.gui.widget.scene import Scene

from LISA.examples.rippler import Rippler
from LISA.examples.heightmap import HeightMap
from LISA.examples.earth import Earth
from LISA.examples.earth_lighting import Earth as EarthLight
from LISA.examples.sprite import Sprites
from LISA.examples.sphere_refinement import SphereRefinement
from LISA.examples.framebuffer import HeightMapFBO

logger = logging.getLogger(__name__)

# read arguments
parser = argparse.ArgumentParser(
    description="To run easily various examples."
)

# commands
parser.add_argument(
    '--Rippler',
    help="Plot the example of the rippler",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--Earth',
    help="Plot the example of the earth",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--HeightMap',
    help="Plot the example of the heightmap",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--Sprites',
    help="Plot the example of the sprites",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--EarthLight',
    help="Plot the example of the earth with widget controls",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--SphereRefinement',
    help="Plot the example of the mesh sphere with refinement",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--HeightMapFBO',
    help="Plot the example of the mesh sphere with refinement",
    action="store_true",
    default=False,
)

# parse command line
args = parser.parse_args()

# create a figure
fig = Figure()

# create an axes
#  axes4 = fig.add_axes(2, 2, 0)
#  axes1 = fig.add_axes(2, 2, 1)
#  axes = fig.add_axes(2, 2, 2)
#  axes2 = fig.add_axes(2, 2, 3)
axes = fig.add_axes(1, 1, 0)

# loop over keys
for key, value in args.__dict__.items():
    if value:
        obj = locals()[key]()
        axes.scene.add(obj)
        try:
            widget = obj.createWidget()
            fig.addWidget(widget)
        except Exception as e:
            trace = traceback.format_exc()
            print("Problem creating widget\n{0}\n{1}".format(trace, e))

        # create a scene
        scene = Scene()
        axes.scene.add(scene)
        scene.add(HeightMap())
        scene.x = 1

        scene2 = Scene()
        scene.add(scene2)
        scene2.add(SphereRefinement())
        scene2.x = 1

input()
