import subprocess
import webbrowser
from pathlib import Path

import pytest

import pyroll.export

pytestmark = pytest.mark.skipif(not pyroll.export.CLI_INSTALLED,
                                reason="pyroll-cli is not installed in the current environment")

INPUT = """
from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence

in_profile = Profile.round(
    diameter=30e-3,
    temperature=1200 + 273.15,
    strain=0,
    material=["C45", "steel"],
    flow_stress=100e6
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
        duration=1
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
"""


def test_cli_json(tmp_path: Path):
    (tmp_path / "input.py").write_text(INPUT)

    result = subprocess.run(("pyroll", "input-py", "solve", "export-json"), cwd=tmp_path)

    result.check_returncode()

    print()
    print((tmp_path / "export.json").read_text())


def test_cli_csv(tmp_path: Path):
    (tmp_path / "input.py").write_text(INPUT)

    result = subprocess.run(("pyroll", "input-py", "solve", "export-csv"), cwd=tmp_path)

    result.check_returncode()

    print()
    print((tmp_path / "export.csv").read_text())


def test_cli_yaml(tmp_path: Path):
    (tmp_path / "input.py").write_text(INPUT)

    result = subprocess.run(("pyroll", "input-py", "solve", "export-yaml"), cwd=tmp_path)

    result.check_returncode()

    print()
    print((tmp_path / "export.yaml").read_text())
