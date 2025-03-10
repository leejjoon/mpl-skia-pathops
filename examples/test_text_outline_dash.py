from mpl_skia_pathops import mpl2skia, skia2mpl, union, difference, stroke_to_fill

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath

fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)

p = TextPath((0, 0), "MA", size=20)

skpath = mpl2skia(p)

skpath2 = stroke_to_fill(skpath, 0.5, linejoin="round", dashes=(0, (4, 2)))
# p2 = skia2mpl(difference(skpath2, skpath))
p2 = skia2mpl(skpath2)

pp2 = PathPatch(p2, fc="w", ec="r")
ax.add_patch(pp2)

ax.set(xlim=(-5, 40), ylim=(-5, 20))
ax.patch.set_fc("gold")

plt.show()

