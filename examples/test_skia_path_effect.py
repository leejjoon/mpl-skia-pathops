from pathops import PathEffect, Path1DPathEffectStyle

from mpl_skia_pathops import mpl2skia, skia2mpl # , union, difference, stroke_to_fill
from mpl_skia_pathops.mpl_skia_pathops import stroke_with_patheffect

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Rectangle, Ellipse
from matplotlib.patches import ArrowStyle


def prepare_axes(ax):
    ax.set_aspect(1)
    ax.set(xlim=(-200, 200), ylim=(-200, 200))
    ax.patch.set_fc("gold")


def get_patch(pe):
    p = Circle((0, 0), radius=100)

    skpath = mpl2skia(p)

    skpath2 = stroke_with_patheffect(skpath, 1, pe, linejoin="round")
    p2 = skia2mpl(skpath2)

    pp2 = PathPatch(p2, fc="r", ec="r")

    return pp2


fig, axs = plt.subplots(2, 2, num=1, clear=True)

# %%

iax = iter(axs.flat)
ax = next(iax)
prepare_axes(ax)


p = Circle((0, 0), radius=10)
pepath = mpl2skia(p)
advance = 30

pe = PathEffect.create_path1d(pepath, advance,
                              style=Path1DPathEffectStyle.TRANSLATE,
                              )
pp2 = get_patch(pe)
ax.add_patch(pp2)

# %%

ax = next(iax)
prepare_axes(ax)


p = Ellipse((0, 0), 30, 15)
pepath = mpl2skia(p)
advance = 42

pe = PathEffect.create_path1d(pepath, advance,
                              style=Path1DPathEffectStyle.ROTATE,
                              )
pp2 = get_patch(pe)
ax.add_patch(pp2)

# %%

ax = next(iax)
prepare_axes(ax)

from matplotlib.patches import ConnectionStyle

path = ConnectionStyle.Arc3().connect((0, 0), (60, 0))
arrow, _ = ArrowStyle.Fancy().transmute(path, 40, 0)

pepath = mpl2skia(arrow)
advance = 79

pe = PathEffect.create_path1d(pepath, advance,
                              style=Path1DPathEffectStyle.MORPH,
                              )
pp2 = get_patch(pe)

ax.add_patch(pp2)

# %%

ax = next(iax)
prepare_axes(ax)


p = Rectangle((0., -10), 2.5, 20)
pepath = mpl2skia(p)
advance = 2

pe = PathEffect.create_path1d(pepath, advance,
                              style=Path1DPathEffectStyle.TRANSLATE,
                              )
pp2 = get_patch(pe)
ax.add_patch(pp2)

plt.show()
