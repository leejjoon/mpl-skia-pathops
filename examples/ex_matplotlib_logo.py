"""
====================
Matplotlib logo in cyberpunk style
====================

"""


import matplotlib.pyplot as plt
from _matplotlib_logo import make_logo

import mplcyberpunk

linewidth_scale = 2


with plt.rc_context():
    plt.style.use("cyberpunk")
    fig, ax = make_logo(height_px=int(110 * linewidth_scale),
                        lw_bars=0.7*linewidth_scale, lw_grid=0.5*linewidth_scale,
                        lw_border=1*linewidth_scale,
                        rgrid=[1, 3, 5, 7], with_text=True)

    cmap = plt.get_cmap()  # we canche the default cmap of the cyberpunk theme.

fig.patch.set(alpha=1) # The figure patch was set to transparent.
ax.patch.set_alpha(0.3)

tp = fig.axes[0].patches[0]  # The textpath
tp.set_clip_on(False)

# make_logo add a circle (rectangle in polar coordinate) patch, that is larger than
# the axes patch (which is a circle). We will use this circle patch to clip the text.

circle = sorted(ax.patches, key=lambda a: a.get_zorder())[0]
circle.set_visible(False)

from mpl_skia_pathops import PathOpsPathEffect
import mpl_visual_context.patheffects as pe
import mpl_visual_context.image_box as ib
import mpl_visual_context.image_effect as ie

glow = pe.ImageEffect(ie.Pad(20*linewidth_scale)
                      | ie.GaussianBlur(10, channel_slice=slice(3, 4))
                      | ie.AlphaAxb((2, 0))
                      | ie.Erosion(50*linewidth_scale, channel_slice=slice(0, 3))
                      )

# We will create an imagebox with the colormap of the cyberpunk theme. We need
# to increase the extent so that the image is large enough when we stroke it.
color_gradient_box = ib.ImageBox("right", extent=[-0.1, -0.1, 1.1, 1.1],
                                 coords=tp, axes=ax, cmap=cmap)

union_circle = PathOpsPathEffect.union(circle)
# stroke2fill = PathOpsPathEffect.stroke2fill()

stroke_color_gradient = (
    union_circle
    | pe.GCModify(linewidth=3*linewidth_scale, alpha=1)
    | PathOpsPathEffect.stroke2fill()
    | pe.FillImage(color_gradient_box)
)

tp.set_path_effects([
    (
        stroke_color_gradient
        | glow
     ),
    (
        union_circle
        | pe.FillImage(color_gradient_box, alpha=0.5)
    ),
    stroke_color_gradient
])


plt.show()

