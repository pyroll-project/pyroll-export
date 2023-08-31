from typing import Any, Sequence

import numpy as np
import pandas as pd
import yaml

from .convert import _to_dict, _flatten_dict
from pyroll.core import Unit, Profile
import json
from typing import Union


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return list(o)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


def to_dict(obj: Union[Unit, Profile]) -> dict[str, Any]:
    """
    Exports a PyRolL Unit or Profile object to a dict tree.
    This is the root export function of this library, all other functions make use of it.
    Conversion of objects can be customized using the ``convert`` plugin hook.

    :param obj: the unit or profile to export
    :returns: the dict representation of the unit
    """
    return _to_dict(obj)


def to_pandas(sequence: Sequence[Unit]) -> pd.DataFrame:
    """
    Exports a PyRolL PassSequence object to a pandas ``DataFrame``.
    Uses a flattened version of the result of ``to_dict()``.
    """
    df = pd.DataFrame([
        _flatten_dict(_to_dict(u)) for u in sequence
    ])
    df.sort_index(axis="columns", inplace=True)
    return df.convert_dtypes()


def to_json(obj: Union[Unit, Profile]) -> str:
    """
    Exports a PyRolL Unit object to a JSON document based on the result of ``to_dict()``.

    :param obj: the unit or profile to export
    :returns: the created JSON document text
    """
    return json.dumps(to_dict(obj), indent=4, cls=JSONEncoder)


def to_yaml(obj: Union[Unit, Profile]) -> str:
    """
    Exports a PyRolL Unit object to a YAML document based on the result of ``to_dict()``.

    :param obj: the unit or profile to export
    :returns: the created YAML document text
    """
    return yaml.dump(to_dict(obj))
