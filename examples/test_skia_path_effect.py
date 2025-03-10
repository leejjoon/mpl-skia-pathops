from pathops import PathEffect, Path1DPathEffectStyle

from mpl_skia_pathops import mpl2skia, skia2mpl # , union, difference, stroke_to_fill
from mpl_skia_pathops.mpl_skia_pathops import stroke_with_patheffect

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Rectangle, Ellipse


fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)

# p = TextPath((0, 0), "MA", size=200)
p = Circle((0, 0), radius=100)
skpath = mpl2skia(p)

# p = Circle((0, 0), radius=5)
# p = Rectangle((0, -2.5), 15, 5)
p = Ellipse((0, 0), 30, 10)
pepath = mpl2skia(p)

# pepath
advance = 100

pe = PathEffect.create_path1d(pepath, 45,
                              # style=Path1DPathEffectStyle.MORPH,
                              style=Path1DPathEffectStyle.ROTATE,
                              )
skpath2 = stroke_with_patheffect(skpath, 1, pe, linejoin="round")

# p2 = skia2mpl(difference(skpath2, skpath))
p2 = skia2mpl(skpath2)

pp2 = PathPatch(p2, fc="w", ec="r")
ax.add_patch(pp2)

ax.set(xlim=(-200, 200), ylim=(-200, 200))
ax.patch.set_fc("gold")

plt.show()

