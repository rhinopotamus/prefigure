from . import (
    annotations,
    area,
    arrow,
    axes,
    calculus,
    circle,
    clip,
    coordinates,
    CTM,
    definition,
    diagram,
    graph,
    grid_axes,
    group,
    implicit,
    label,
    label_tools,
    line,
    math_utilities,
    parametric_curve,
    parse,
    path,
    point,
    polygon,
    read,
    rectangle,
    repeat,
    riemann_sum,
    slope_field,
    statistics,
    tags,
    tangent_line,
    user_namespace,
    utilities,
    vector
)

import logging
log = logging.getLogger("prefigure")

try:
    from . import (
        diffeqs,
        network,
        shape
    )
except:
    # We're probably in the pyodide environment.  We will report in tags
    pass
