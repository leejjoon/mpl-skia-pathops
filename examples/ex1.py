"""
====================
Simple patheffect example
====================

"""

import matplotlib.pyplot as plt
import mpl_visual_context.patheffects  as pe
from matplotlib.transforms import Affine2D
from mpl_skia_pathops import PathOpsPathEffect
# from mpl_skia_pathops import PathOps


fig, axs = plt.subplots(2, 1, num=1, clear=True)

ax = axs[0]
t = ax.text(0.5, 0.5, "Matplotib", size=50, ha="center", va="center")
t.set_bbox(dict(facecolor='none', ec="none"))

def bbox():
    return t.get_bbox_patch()

t.set_path_effects([PathOpsPathEffect.difference(bbox, invert=True) | pe.Gradient("right")])


ax = axs[1]
t2 = ax.text(0.5, 0.5, "Matplotib", size=50, ha="center", va="center")
t2.set_bbox(dict(facecolor='none', ec="none"))


def bbox_half():
    "we get the rectangle that spans the bottom half of the text bbox"
    p = t2.get_bbox_patch()
    path = p.get_path()
    ymin = path.vertices[: -1].min()
    affine = Affine2D().translate(0, -ymin).scale(1, 0.5).translate(0, ymin)
    tr = p.get_transform()
    return (affine + tr).transform_path(path)


t2.set_path_effects([PathOpsPathEffect.xor(bbox_half, invert=True) | pe.Gradient("right")])

plt.show()


