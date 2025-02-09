import numpy as np
from pathops import (
    Path,
    OpBuilder,
    PathOp,
    PathOpsError,
    LineCap,
    LineJoin
)

from matplotlib.path import Path as MPath

def mpl2skia(mpl_path, transform=None):
    if transform is not None:
        mpl_path = transform.transform_path(mpl_path)

    ci = iter(mpl_path.codes)
    vi = iter(mpl_path.vertices)

    path = Path()
    pen = path.getPen()

    for c in ci:
        if c == MPath.MOVETO:
            pen.moveTo(next(vi))
        elif c == MPath.LINETO:
            pen.lineTo(next(vi))
        elif c == MPath.CURVE3:
            pen.qCurveTo(next(vi), next(vi))
            next(ci)
        elif c == MPath.CURVE4:
            pen.curveTo(next(vi), next(vi), next(vi))
            next(ci)
            next(ci)
        elif c == MPath.CLOSEPOLY:
            pen.closePath()
            next(vi)

    return path

from pathops._pathops import SegmentPenIterator

def skia2mpl(skia_path):
    codes = []
    verts = []

    # segments iterator does some simplification, which make things more complicated.
    # We use SegmentPenIterator, instead.
    for s, cc in list(SegmentPenIterator(skia_path)):

        if s == "moveTo":
            codes.extend([MPath.MOVETO] * len(cc))
            verts.extend(cc)
        elif s == "lineTo":
            codes.extend([MPath.LINETO] * len(cc))
            verts.extend(cc)
        elif s == "qCurveTo":
            if len(cc) == 2:
                codes.extend([MPath.CURVE3, MPath.CURVE3])
                verts.extend(cc)
            elif len(cc) > 2:
                # if len(c) > 2, multiple quad curve points are returned with
                # midpoints skipped and concatenated.
                ccc = []
                for i in range(0, len(cc)-2):
                    cc1 = cc[i]
                    cc2 = cc[i+1]
                    cc12 = 0.5*(np.array(cc1) + np.array(cc2)) # make midpoint
                    ccc.extend([cc1, cc12])
                ccc.extend(cc[-2:])

                verts.extend(ccc)
                codes.extend([MPath.CURVE3] * len(ccc))

        elif s == "curveTo":
            codes.extend([MPath.CURVE4] * len(cc))
            verts.extend(cc)
        elif s == "closePath":
            codes.append(MPath.CLOSEPOLY)
            verts.extend([(0, 0)])

    p = MPath(verts, codes=codes)
    return p


def union(path1, path2,
          fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.UNION)
    result = builder.resolve()

    return result


def union_all(pathlist,
              fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    for path in pathlist:
        builder.add(path, PathOp.UNION)
    result = builder.resolve()

    return result


def intersection(path1, path2,
                 fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.INTERSECTION)
    result = builder.resolve()

    return result

def difference(path1, path2,
               fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.DIFFERENCE)
    result = builder.resolve()

    return result

def xor(path1, path2,
        fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.XOR)
    result = builder.resolve()

    return result


_TO_SKIA_LINE_CAP = {
    "butt": LineCap.BUTT_CAP,
    "round": LineCap.ROUND_CAP,
    "square": LineCap.SQUARE_CAP,
}

_TO_SKIA_LINE_JOIN = {
    "miter": LineJoin.MITER_JOIN,
    "round": LineJoin.ROUND_JOIN,
    "bevel": LineJoin.BEVEL_JOIN,
    # No arcs or miter-clip
}

def stroke_to_fill(skpath, stroke_width: float,
                   fractional_tolerence: float = 0.1,
                   linejoin: str = "round",
                   linecap: str = "round",
                   fractional_miterlimit: float = 1.,
                   ):
    tolerance = stroke_width * fractional_tolerence
    miterlimit = stroke_width * fractional_miterlimit
    skpath = Path(skpath)
    dash_array = ()
    dash_offset = 0.0
    skpath.stroke(stroke_width,
                  _TO_SKIA_LINE_CAP[linecap],
                  _TO_SKIA_LINE_JOIN[linejoin],
                  miterlimit, dash_array, dash_offset)

    skpath.convertConicsToQuads(tolerance)

    backup = Path(skpath)
    try:
        skpath.simplify(fix_winding=True)
    except PathOpsError:
        # skip tricky paths that trigger PathOpsError
        # https://github.com/googlefonts/picosvg/issues/192
        skpath = backup

    return skpath
