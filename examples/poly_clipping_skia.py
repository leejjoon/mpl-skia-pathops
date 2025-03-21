"""
====================
Path clipping example
====================

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

from matplotlib.patches import (PathPatch, Circle, Rectangle, Ellipse)
from matplotlib.path import Path

from mpl_skia_pathops import SkiaPath

# We will define shapes with Matplotlib. `mpl-skia-pathops` does not provide a
# convenient way to create shapes. Either you create skia path by your self, or
# create a Matplotlib Patch/Path and convert them to Skia one. We will follow
# the latter approach.

# Boundary is required if and only if you want to invert the path.
boundary_ext = [-1.5, 1.5, -1, 1]
boundary = Rectangle((boundary_ext[0], boundary_ext[2]),
                     width=boundary_ext[1] - boundary_ext[0],
                     height=boundary_ext[3] - boundary_ext[2]
                     )

a = Circle((-0.5, 0), radius=0.75)
# b = Rectangle((-0.2, -0.5), 1.2, 1.)
b = Ellipse((0.5, 0), 1.5, 1.2)

# a concatenation of two paths.
a_b = Path.make_compound_path(
    a.get_patch_transform().transform_path(a.get_path()),
    b.get_patch_transform().transform_path(b.get_path())
)

# Now we convert these to skia path.
skia_boundary = SkiaPath.from_mpl(boundary)

A = SkiaPath.from_mpl(a)
A.set_boundary(skia_boundary)
B = SkiaPath.from_mpl(b)
B.set_boundary(skia_boundary)

# Path effect.
import mpl_visual_context.patheffects as pe

path_effects = [pe.FillOnly() | pe.GCModify(alpha=0.3),
                pe.StrokeOnly()]

# list of operations

operations = [
    ("A", lambda A, B: A),
    ("B", lambda A, B: B),
    ("¬A", lambda A, B: ~A),
    ("¬B", lambda A, B: ~B),
    ("A ∪ B", lambda A, B: A | B),
    ("A ∪ ¬B", lambda A, B: A | ~B),
    ("¬A ∪ B", lambda A, B: ~A | B),
    ("¬A ∪ ¬B", lambda A, B: ~A | ~B),
    ("A ∩ B", lambda A, B: A & B),
    ("A ∩ ¬B", lambda A, B: A & ~B),
    ("¬A ∩ B", lambda A, B: ~A & B),
    ("¬A ∩ ¬B", lambda A, B: ~A & ~B),
    ("A ^ B", lambda A, B: A ^ B),
    ("A.stroke()", lambda A, B: A.stroke(stroke_width=0.3)),
    ("B.dilate()", lambda A, B: B.dilate(stroke_width=0.4)),
    ("B.erode()", lambda A, B: B.erode(stroke_width=0.4))
]


# plot

fig, axs = plt.subplots(4, 4, num=1, clear=True, layout="constrained")
for ax, (label, op) in zip(axs.flat, operations):
    ax.set_aspect(1)

    # we first add the concatenated one.
    p = PathPatch(a_b, fc="none", ec="0.8", ls="--", lw=2, zorder=1)
    ax.add_patch(p)

    # now the one with the operation applied.
    cc = op(A, B)
    p = PathPatch(cc.to_mpl(), fc="0.8", ec="k", lw=2, zorder=2, clip_on=False)
    ax.add_patch(p)
    p.set_path_effects(path_effects)

    ax.set(title=label, xlim=boundary_ext[:2], ylim=boundary_ext[2:])
    ax.tick_params(left=False, bottom=False, labelbottom=False, labelleft=False)

plt.show()
