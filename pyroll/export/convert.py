import inspect
from dataclasses import is_dataclass
from typing import Any, Union
from collections.abc import Sequence, Set, Mapping

import numpy as np
import shapely

from pyroll.export.pluggy import hookimpl, plugin_manager
from pyroll.core.repr import ReprMixin


def _to_dict(instance: ReprMixin):
    return {
        "type": type(instance).__qualname__
    } | {
        n: c for n, v in instance.__attrs__.items()
        if (c := plugin_manager.hook.convert(name=n, value=v, parent=instance)) is not None
    }


def _flatten_dict(d: dict[str, Any]) -> dict[Union[str, tuple[str, ...]], Any]:
    def _gen(d_: dict[str, Any], prefix=()):
        for k, v in d_.items():
            if isinstance(v, dict):
                yield from _gen(v, prefix + (k,))
            elif k == "disk_elements":
                for i, de in enumerate(v):
                    yield from _gen(de, prefix + (k, str(i)))
            else:
                yield prefix + (k,), v

    return dict(("_".join(k), v) for k, v in _gen(d))


@hookimpl(specname="convert")
def convert_shapely_line_string(value: object):
    if isinstance(value, shapely.LineString):
        return dict(
            length=value.length,
            height=value.bounds[3] - value.bounds[1],
            width=value.bounds[2] - value.bounds[0],
            x=np.array(value.xy[0]),
            y=np.array(value.xy[1]),
            xy=np.array(value.xy),
            coords=np.array(value.coords),
        )


@hookimpl(specname="convert")
def convert_shapely_multi_line_string(value: object):
    if isinstance(value, shapely.MultiLineString):
        return dict(
            length=value.length,
            height=value.bounds[3] - value.bounds[1],
            width=value.bounds[2] - value.bounds[0],
            x=[np.array(ls.xy[0]) for ls in value.geoms],
            y=[np.array(ls.xy[1]) for ls in value.geoms],
            xy=np.concatenate([np.array(ls.xy) for ls in value.geoms], axis=1),
            coords=np.concatenate([np.array(ls.coords) for ls in value.geoms], axis=0),
        )


@hookimpl(specname="convert")
def convert_shapely_polygon(value: object):
    if isinstance(value, shapely.Polygon):
        return dict(
            area=value.area,
            perimeter=value.length,
            height=value.bounds[3] - value.bounds[1],
            width=value.bounds[2] - value.bounds[0],
            x=np.array(value.exterior.coords.xy[0]),
            y=np.array(value.exterior.coords.xy[1]),
            xy=np.array(value.exterior.coords.xy),
            coords=np.array(value.exterior.coords),
        )


@hookimpl(specname="convert")
def convert_shapely_multi_polygon(value: object):
    if isinstance(value, shapely.MultiPolygon):
        return dict(
            area=value.area,
            perimeter=value.length,
            height=value.bounds[3] - value.bounds[1],
            width=value.bounds[2] - value.bounds[0],
            x=[np.array(ls.exterior.coords.xy[0]) for ls in value.geoms],
            y=[np.array(ls.exterior.coords.xy[1]) for ls in value.geoms],
            xy=np.concatenate([np.array(pg.exterior.coords.xy) for pg in value.geoms], axis=1),
            coords=np.concatenate([np.array(pg.exterior.coords) for pg in value.geoms], axis=0),
        )


@hookimpl(specname="convert")
def convert_shapely_point(value: object):
    if isinstance(value, shapely.Point):
        return np.array([value.x, value.y])


@hookimpl(specname="convert")
def convert_shapely_multi_point(value: object):
    if isinstance(value, shapely.MultiPoint):
        return np.array([(p.x, p.y) for p in value.geoms])


@hookimpl(specname="convert")
def convert_repr_mixin(value: object):
    if isinstance(value, ReprMixin):
        return _to_dict(value)


@hookimpl(specname="convert")
def convert_mapping(name: str, value: object):
    if isinstance(value, Mapping):
        return {n: plugin_manager.hook.convert(name=f"{name}[{n}]", value=v, parent=value) for n, v in value.items()}


@hookimpl(specname="convert")
def convert_sequence(name: str, value: object):
    if (
            (isinstance(value, Sequence) or isinstance(value, Set))
            and not isinstance(value, str)
            and not isinstance(value, np.ndarray)
    ):
        return [plugin_manager.hook.convert(name=f"{name}[{i}]", value=v, parent=value) for i, v in enumerate(value)]


@hookimpl(specname="convert")
def convert_numpy_array(name: str, value):
    if isinstance(value, np.ndarray):
        squeezed = value.squeeze()
        if squeezed.ndim == 0:
            return plugin_manager.hook.convert(name=name, value=squeezed[()], parent=value)
        return value


@hookimpl(specname="convert")
def convert_primitives(value):
    if isinstance(value, np.number):
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.integer):
            return int(value)
    if isinstance(value, (float, str, int, bool, bytes)):
        return value


@hookimpl(specname="convert")
def convert_dataclass(value):
    if is_dataclass(value):
        return dict(value.__dict__)


@hookimpl(specname="convert")
def convert_callable(value, parent):
    if callable(value):
        if len(inspect.signature(value).parameters) == 0:
            return value()
        else:
            return value(parent)
