import logging

import typer

from swegov_opendata.infrastructure.kernel.telemetry import (
    TelemetryConfig,
    configure_logging,
)

logger = logging.getLogger(__name__)


def create_app() -> typer.Typer:
    app = typer.Typer(callback=set_app_context)

    from swegov_opendata.presentation.console.commands import sfs

    app.add_typer(sfs.app, name="sfs")
    return app


def set_app_context(ctx: typer.Context, *, debug: bool = False):
    ctx.obj = {"debug": debug}
    configure_logging(TelemetryConfig(level="DEBUG" if debug else "WARN"))


app = create_app()


if __name__ == "__main__":
    app()
