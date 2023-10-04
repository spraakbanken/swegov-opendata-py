from dataclasses import dataclass
import logging
from logging.config import dictConfig
from typing import Union


@dataclass()
class TelemetryConfig:
    level: Union[str, int]


def configure_logging(config: TelemetryConfig) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] %(message)s",  # noqa: E501
                },
                "standard": {
                    "class": "swegov_opendata.infrastructure.kernel.telemetry.ExFormatter",
                    "format": "%(asctime)s-%(levelname)s-%(name)s(%(lineno)d): %(message)s",  # noqa: E501
                    # "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s",  # noqa: E501
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "swegov_opendata": {
                    "handlers": ["console"],
                    "level": config.level,
                    "propagate": True,
                },
                # third-party package loggers
            },
        }
    )


class ExFormatter(logging.Formatter):
    def_keys = [
        "asctime",
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "message",
    ]

    def format(self, record):
        string = super().format(record)
        extra = {k: v for k, v in record.__dict__.items() if k not in self.def_keys}
        if len(extra) > 0:
            string += " - extra: " + str(extra)
        return string
