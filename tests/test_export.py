import subprocess
import webbrowser
from pathlib import Path

import numpy as np

import pyroll.export

from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence

in_profile = Profile.round(
    diameter=30e-3,
    temperature=1200 + 273.15,
    strain=0,
    material=["C45", "steel"],
    flow_stress=100e6,
    chemical_composition={
        "Fe": 0.95,
        "Cr": 0.05,
    }
)

sequence = PassSequence([
    RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
    Transport(
        label="I => II",
        duration=1,
        array_values=np.array([1, 2, 3, 4]),
        zero_d_array=np.array(4),
    ),
    RollPass(
        label="Round II",
        roll=Roll(
            groove=RoundGroove(
                r1=1e-3,
                r2=12.5e-3,
                depth=11.5e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
])

sequence.solve(in_profile)


def test_json(tmp_path: Path):
    exported = pyroll.export.to_json(sequence)

    print()
    print(exported)


def test_pandas(tmp_path: Path):
    exported = pyroll.export.to_pandas(sequence)

    f = (tmp_path / "df.html")
    f.write_text(exported.to_html())
    webbrowser.open(f.as_uri())


def test_toml(tmp_path: Path):
    exported = pyroll.export.to_toml(sequence)

    print()
    print(exported)


def test_yaml(tmp_path: Path):
    exported = pyroll.export.to_yaml(sequence)

    print()
    print(exported)