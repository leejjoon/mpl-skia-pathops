import matplotlib.pyplot as plt
import mpl_visual_context.patheffects  as pe
from matplotlib.transforms import Affine2D
from mpl_skia_pathops import PathOps


fig, ax = plt.subplots(num=1, clear=True)
t = ax.text(0.5, 0.5, "Matplotib", size=50, ha="center", va="center")
t.set_bbox(dict(facecolor='none', ec="none", alpha=0.5))

def func():
    "we get the rectangle that spans the bottom half of the text bbox"
    p = t.get_bbox_patch()
    path = p.get_path()
    ymin = path.vertices[: -1].min()
    affine = Affine2D().translate(0, -ymin).scale(1, 0.5).translate(0, ymin)
    tr = p.get_transform()
    return (affine + tr).transform_path(path)

po = PathOps.from_func(func)
# po = PathOps.from_mpl_patch(t.get_bbox_patch())

t.set_path_effects([po.get_path_effect("xor") | pe.Gradient("right")])
# t.set_path_effects([po.get_path_effect("difference") | pe.Gradient("right")])

plt.show()


