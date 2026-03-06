import logging
from pathlib import Path

import typer

from swegov_opendata.infrastructure.kernel import telemetry
from swegov_opendata.infrastructure.kernel.telemetry import TelemetryConfig

logger = logging.getLogger(__name__)


def create_app() -> typer.Typer:
    app = typer.Typer(callback=set_app_context)

    from swegov_opendata.presentation.console.commands import rd, sfs

    app.add_typer(sfs.app, name="sfs")
    app.add_typer(rd.app, name="rd")
    return app


_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def set_app_context(ctx: typer.Context, *, debug: bool = False):
    ctx.obj = {"debug": debug}
    # telemetry.configure_logging(
    telemetry.configure_telemetry(
        TelemetryConfig(
            level="DEBUG" if debug else "WARN",
            project_name="swegov_opendata",
            project_root=_PROJECT_ROOT,
        )
    )


app = create_app()


if __name__ == "__main__":
    print(f"{_PROJECT_ROOT=}")
    # app()gcc
