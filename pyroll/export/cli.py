import logging
from pathlib import Path

from pyroll.cli import State
import click
from .export import to_json, to_pandas, to_yaml

DEFAULT_EXPORT_FILE = Path("export")


@click.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_EXPORT_FILE.with_suffix(".json"), show_default=True
)
@click.pass_obj
def export_json(state: State, file: Path):
    """Exports the simulation results to JSON and writes them to FILE."""
    log = logging.getLogger(__name__)

    exported = to_json(state.sequence)

    file.write_text(exported, encoding='utf-8')
    log.info(f"Wrote export to: {file.absolute()}")


@click.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_EXPORT_FILE.with_suffix(".csv"), show_default=True
)
@click.pass_obj
def export_csv(state: State, file: Path):
    """Exports the simulation results to JSON and writes them to FILE."""
    log = logging.getLogger(__name__)

    exported = to_pandas(state.sequence)

    exported.to_csv(file)
    log.info(f"Wrote export to: {file.absolute()}")


@click.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_EXPORT_FILE.with_suffix(".yaml"), show_default=True
)
@click.pass_obj
def export_yaml(state: State, file: Path):
    """Exports the simulation results to YAML and writes them to FILE."""
    log = logging.getLogger(__name__)

    exported = to_yaml(state.sequence)

    file.write_text(exported, encoding='utf-8')
    log.info(f"Wrote export to: {file.absolute()}")
