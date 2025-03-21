"""
====================
Text Shade
====================

"""

import numpy as np

# from mpl_visual_context.patheffects import FillColor, AlphaGradient
import mpl_visual_context.patheffects as pe
from mpl_visual_context.patheffects_shadow import ShadowPath
from mpl_skia_pathops import PathOpsPathEffect

import matplotlib.pyplot as plt

class Clipboard(pe.Clipboard):
    def get_path(self):
        tpath = self["tpath"]
        affine = self["affine"]
        return affine.transform_path(tpath)


red = np.array([233, 77, 85, 255]) / 255
darkred = np.array([130, 60, 71, 255]) / 255

fig, axs = plt.subplots(2, 1, num=2, clear=True)
ax = axs[0]
t = ax.text(0.5, 0.5, "Matplotlib", ha="center", va="center",
            size=40, color="w", clip_on=True)

cb = Clipboard()

t.set_path_effects([cb.copy() | ShadowPath(45, 5) | pe.FillColor(darkred) |
                    PathOpsPathEffect.difference(cb.get_path),
                    # | AlphaGradient("0 ^ 0.1 ^ 0.3 ^ 0.5"),
                    # Normal(),
                    ])

# ax.patch.set_fc(red)
ax.patch.set_fc(red)


ax = axs[1]

t = np.linspace(0, 2 * np.pi, 1024)
data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

im = ax.imshow(data2d, aspect="auto")

size = 32

ann1 = ax.annotate("A", (0, 1),
                   xycoords="axes fraction", size=size,
                   xytext=(5, -5), textcoords="offset points", va="top")

ann2 = ax.annotate("A", (0, 1),
                   xycoords="axes fraction", size=size,
                   xytext=(5+size, -5), textcoords="offset points", va="top")

ann3 = ax.annotate("A", (0, 1),
                   xycoords="axes fraction", size=size,
                   xytext=(5+2*size, -5), textcoords="offset points", va="top")

ann4 = ax.annotate("A", (0, 1),
                   xycoords="axes fraction", size=size,
                   xytext=(5+3*size, -5), textcoords="offset points", va="top")

ann2.set_path_effects([pe.GCModify(linewidth=0.5) | pe.StrokeOnly()])

cb = Clipboard()
ann3.set_path_effects([cb.copy() | ShadowPath(45, 1) | pe.FillColor("k") |
                       PathOpsPathEffect.difference(cb.get_path),
                       ])

cb = Clipboard()
ann4.set_path_effects([cb.copy() | ShadowPath(45, 1) | pe.FillColor("k") |
                       PathOpsPathEffect.difference(cb.get_path),
                       pe.GCModify(alpha=0.5) | pe.FillColor("w") | pe.FillOnly()
                       ])

plt.show()
