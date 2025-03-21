"""
====================
Simple patheffect example
====================

"""
import matplotlib.pyplot as plt

import numpy as np

import mpl_visual_context.patheffects as pe
from mpl_skia_pathops import PathOpsPathEffect

# Fixing random state for reproducibility
np.random.seed(19680)

# Example data
n = 4
"""
====================
another patheffect example
====================

"""
x_pos = np.arange(n)
performance = 5 * np.random.rand(n)
colors = [f"C{i}" for i in range(n)]

fig, ax = plt.subplots(num=1, clear=True)

bars = ax.bar(x_pos, performance, align='center', alpha=0.7, color=colors)


cb = pe.Clipboard()

def get_path_from_cb():
    path = cb["tpath"]
    affine = cb["affine"]
    return affine.transform_path(path)

pe = [pe.RoundCorner(20, i_selector=lambda i: i in [2, 3]) | cb.copy()
      | pe.HLSModify(l=0.7),
      pe.RoundCorner(20, i_selector=lambda i: i in [2, 3]) |  pe.Offset(5, -5)
      | PathOpsPathEffect.difference(get_path_from_cb, invert=True) | pe.GCModify(alpha=0.2),
      ]

for p in bars[:]:
    p.set_path_effects(pe)

plt.show()
