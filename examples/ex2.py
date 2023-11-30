import matplotlib.pyplot as plt

import mpl_visual_context.patheffects as pe
from mpl_visual_context.patheffects_image_box import AlphaGradient
from mpl_visual_context.patheffects import RoundCorner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patheffects import Normal

# Fixing random state for reproducibility
np.random.seed(19680)

# Example data
n = 4
x_pos = np.arange(n)
performance = 5 * np.random.rand(n)
colors = [f"C{i}" for i in range(n)]

fig, ax = plt.subplots(num=1, clear=True)

bars = ax.bar(x_pos, performance, align='center', alpha=0.7, color=colors)

from mpl_skia_pathops import PathOps
po = PathOps()

pe = [RoundCorner(20, i_selector=lambda i: i in [2, 3]) | po.get_path_effect("update_from")
      | pe.HLSModify(l=0.7),
      RoundCorner(20, i_selector=lambda i: i in [2, 3]) |  pe.Offset(5, -5)
      | po.get_path_effect("difference") | pe.GCModify(alpha=0.2),
      ]

#  | AlphaGradient("0.2 ^ 1.")]
for p in bars[:1]:
    p.set_path_effects(pe)

plt.show()
