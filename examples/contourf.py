import numpy as np
import matplotlib.pyplot as plt
import mpl_visual_context.patheffects as pe
from mpl_skia_pathops import SkiaShadow # make_shadow_patheffects

def make_shadow_patheffects(
        fc_white="w",
        fc_black="0.2",
        alpha=0.5,
        offset=2.5,
        angle=135):

    patheffects = [
        (SkiaShadow(offset, angle)
         | pe.FillColor(fc_black)
         | pe.GCModify(alpha=alpha)),
        (SkiaShadow(offset, 180+angle)
         | pe.FillColor(fc_white)
         | pe.GCModify(alpha=alpha)),
    ]

    return patheffects


from matplotlib.contour import QuadContourSet
from matplotlib.patches import PathPatch, Polygon
from matplotlib.path import Path

# Data
X, Y = np.meshgrid(np.linspace(-5, 10, 100),
                   np.linspace(-5, 10, 100))
Z = -np.sqrt(X ** 2 + Y ** 2)

# Contour
fig, axs = plt.subplots(1, 2, num=2, clear=True)

ax = axs[0]
ax.set_aspect(1)
contours = ax.contourf(X, Y, Z)

from mpl_inner_title import add_inner_title
at = add_inner_title(ax, "A", loc=2, style=None, extra_prop=dict(color="w", size=20),
                     extra_kwargs=dict(frameon=False))

patheffects = make_shadow_patheffects(fc_black="k", offset=1, angle=45, alpha=0.8)[:]
t = at.txt._text

# t = ax.text(2, 2, "A", fontsize=30, color="none")
# t.set_path_effects(patheffects + [pe.FillOnly()])
t.set_path_effects(patheffects)


ax = axs[1]
ax.set_aspect(1)
contours = ax.contourf(X, Y, Z)
# contours.remove()

# %%


def add_contour_shadow(ax, contours,
                       fc_white="w",
                       fc_black="0.2",
                       alpha=0.5,
                       offset=2.5,
                       angle=135):

    # we first create patches for the shadow
    zorder = contours.zorder

    for level, c in zip(contours.levels, contours.get_facecolors()):

        sub_contours = QuadContourSet(ax, X, Y, Z,
                                      levels=[level, np.inf],
                                      filled=True)
        sub_contours.remove() # the contour is added to the axes by default. We do not want that.

        segs = sub_contours.allsegs[0] # Essentially there is a single level.

        paths = []
        for seg in segs:
            if len(seg):
                poly = Polygon(seg, fc=c, ec="none")
                paths.append(poly.get_path())

        if paths: # we combine the paths.
            path = Path.make_compound_path(*paths)
            ax.add_patch(PathPatch(path, fc=c, ec="none", zorder=zorder+1))

    # Now we add patheffects.

    patheffects = make_shadow_patheffects(
        fc_white,
        fc_black,
        alpha,
        offset,
        angle
    )

    for p in ax.patches:
        p.set_path_effects(patheffects)


add_contour_shadow(ax, contours, angle=45)

plt.show()
