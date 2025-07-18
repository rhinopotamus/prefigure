import logging
import lxml.etree as ET
from . import annotations
from . import area
from . import axes
from . import clip
from . import circle
from . import coordinates
from . import CTM
from . import definition
from . import graph
from . import grid_axes
from . import group
from . import implicit
from . import label
from . import legend
from . import line
from . import path
from . import parametric_curve
from . import point
from . import polygon
from . import read
from . import rectangle
from . import riemann_sum
from . import repeat
from . import slope_field
from . import statistics
from . import tangent_line
from . import vector

# this dictionary associates tags to a function that processes
#   elements having that tag

tag_dict = {
    'angle-marker': circle.angle,
    'annotations': annotations.annotations,
    'arc': circle.arc,
    'area-between-curves': area.area_between_curves,
    'area-under-curve': area.area_under_curve,
    'axes': axes.axes,
    'caption': label.caption,
    'circle': circle.circle,
    'clip': clip.clip,
    'coordinates': coordinates.coordinates,
    'definition': definition.definition,
    'derivative': definition.derivative,
    'ellipse': circle.ellipse,
    'graph': graph.graph,
    'grid': grid_axes.grid,
    'grid-axes': grid_axes.grid_axes,
    'group': group.group,
    'histogram': statistics.histogram,
    'implicit-curve': implicit.implicit_curve,
    'label': label.label,
    'legend': legend.legend,
    'line': line.line,
    'parametric-curve': parametric_curve.parametric_curve,
    'path': path.path,
    'point': point.point,
    'polygon': polygon.polygon,
    'read': read.read,
    'rectangle': rectangle.rectangle,
    'repeat': repeat.repeat,
    'riemann-sum': riemann_sum.riemann_sum,
    'tick-mark': axes.tick_mark,
    'transform': CTM.transform_group,
    'rotate': CTM.transform_rotate,
    'scale': CTM.transform_scale,
    'scatter': statistics.scatter,
    'slope-field': slope_field.slope_field,
    'spline': polygon.spline,
    'tangent-line': tangent_line.tangent,
    'translate': CTM.transform_translate,
    'triangle': polygon.triangle,
    'vector': vector.vector
}

log = logging.getLogger('prefigure')

try:
    from . import diffeqs
    from . import network
    from . import shape
    tag_dict['de-solve'] = diffeqs.de_solve
    tag_dict['define-shapes'] = shape.define
    tag_dict['network'] = network.network
    tag_dict['plot-de-solution'] = diffeqs.plot_de_solution
    tag_dict['shape'] = shape.shape
except:
    log.info("Unable to work with differential equations, networks, and shapes")
    log.info("Most likely we are working in a wasm environment")

# apply the processing function based on the XML element's tag

def parse_element(element, diagram, root, outline_status = None):
    if element.tag is ET.Comment:
        return
    if path.is_path_tag(element.tag):
        log.warning(f"A <{element.tag}> tag can only occur inside a <path>")
        return
    if label.is_label_tag(element.tag):
        log.warning(f"A <{element.tag}> tag can only occur inside a <label>")
        return
    if grid_axes.is_axes_tag(element.tag):
        log.warning(f"A <{element.tag}> tag can only occur inside a <axes> or <grid-axes>")
        return

    try:
        function = tag_dict[element.tag]
    except KeyError:
        log.error('Unknown element tag: ' + element.tag)
        return

    if log.getEffectiveLevel() == logging.DEBUG:
        tag = element.tag
        if element.tag == 'definition':
            if element.text is None:
                log.error("PreFigure is ignoring an empty definition")
                return
            text = element.text.strip()
            msg = f"Processing definition: {text}"
        else:
            msg = f"Processing element {element.tag}"
            at = element.get('at', None)
            if at is not None:
                msg += f" with handle {at}"

        log.debug(msg)

    function(element, diagram, root, outline_status)
