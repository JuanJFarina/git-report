import logging

import typer
from typing_extensions import Annotated

from . import __version__
from .git_report import run

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    since_last_merge: Annotated[
        bool,
        typer.Option("--last-merge", "-lm", help="Get git report since last merge"),
    ] = True,
    since_n_days: Annotated[
        str, typer.Option("--since", "-s", help="Get git report since n days")
    ] = "-1",
    version: Annotated[
        bool, typer.Option("--version", "-V", help="Shows the version of git-report")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Print INFO logging statements")
    ] = False,
    extra_verbose: Annotated[
        bool, typer.Option("-vv", help="Print DEBUG logging statements")
    ] = False,
) -> None:
    """Returns a report with all commits authors, amount of commits, percentage of total
    , and also number of files changed, lines added and lines deleted"""

    if version:
        typer.echo(__version__)
        raise typer.Exit

    if verbose:
        logging.basicConfig(level=logging.INFO)

    if extra_verbose:
        logging.basicConfig(level=logging.DEBUG)

    if since_last_merge:
        run(since_n_days)

    raise typer.Exit


if __name__ == "__main__":
    app()
