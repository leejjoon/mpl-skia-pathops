"""
====================
Text Outline
====================

"""

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath

from mpl_skia_pathops import SkiaPath

fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)

p = TextPath((0, 0), "MA", size=20)

sp = SkiaPath.from_mpl(p)
sp2 = sp.stroke(1.5, linejoin="round") - sp

pp2 = PathPatch(sp2.to_mpl(), fc="w", ec="r")
ax.add_patch(pp2)

ax.set(xlim=(-5, 40), ylim=(-5, 20))
ax.patch.set_fc("gold")

plt.show()

