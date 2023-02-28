from typing import Any, Union
from collections.abc import Sequence, Set, Mapping

import numpy as np
from shapely.lib import Geometry

from pyroll.export.pluggy import hookimpl, plugin_manager
from pyroll.core.repr import ReprMixin


def _to_dict(instance: ReprMixin):
    return {
        "type": type(instance).__qualname__
    } | {
        n: c for n, v in instance.__attrs__.items()
        if (c := plugin_manager.hook.convert(name=n, value=v)) is not None
    }


def _flatten_dict(d: dict[str, Any]) -> dict[Union[str, tuple[str, ...]], Any]:
    def _gen(d_: dict[str, Any], prefix=()):
        for k, v in d_.items():
            if isinstance(v, dict):
                yield from _gen(v, prefix + (k,))
            else:
                yield prefix + (k,), v

    return dict((".".join(k), v) for k, v in _gen(d))


@hookimpl(specname="convert")
def convert_shapely(value: object):
    if isinstance(value, Geometry):
        return _to_dict(value)


@hookimpl(specname="convert")
def convert_repr_mixin(value: object):
    if isinstance(value, ReprMixin):
        return _to_dict(value)


@hookimpl(specname="convert")
def convert_mapping(name: str, value: object):
    if isinstance(value, Mapping):
        return {n: plugin_manager.hook.convert(name=f"{name}[{n}]", value=v) for n, v in value.items()}


@hookimpl(specname="convert")
def convert_sequence(name: str, value: object):
    if (isinstance(value, Sequence) or isinstance(value, Set)) and not isinstance(value, str):
        return [plugin_manager.hook.convert(name=f"{name}[{i}]", value=v) for i, v in enumerate(value)]


@hookimpl(specname="convert")
def convert_numpy_array(name: str, value):
    if isinstance(value, np.ndarray):
        squeezed = value.squeeze()
        if squeezed.ndim == 0:
            return plugin_manager.hook.convert(name=name, value=squeezed[()])
        return [plugin_manager.hook.convert(name=f"{name}[{i}]", value=value[i]) for i in range(len(value))]


@hookimpl(specname="convert")
def convert_primitives(value):
    if isinstance(value, np.number):
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.integer):
            return int(value)
    if isinstance(value, (float, str, int, bool, bytes)):
        return value