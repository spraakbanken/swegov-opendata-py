import logging
import socket
import sys
import typing as t
from dataclasses import dataclass
from logging.config import dictConfig
from pathlib import Path

import structlog
from json_arrays import jsonlib
from structlog.typing import EventDict


@dataclass()
class TelemetryConfig:
    level: str
    project_root: Path
    project_name: str


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
                    "format": "%(asctime)s-%(levelname)s-%(name)s(%(lineno)d): %(message)s",
                    # "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s",  # noqa: E501
                },
                "bunyan": {
                    "()": "bunyan_formatter.BunyanFormatter",
                    "project_name": config.project_name,
                    "project_root": config.project_root,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "bunyan",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "preprocess-rd.log",
                    "encoding": "utf-8",
                    "formatter": "bunyan",
                    "mode": "w",
                },
            },
            "loggers": {
                "swegov_opendata": {
                    "handlers": ["file"],
                    "level": config.level,
                    "propagate": True,
                },
                # third-party package loggers
            },
        }
    )


LEVEL_MAP = {
    "TRACE": 10,
    "DEBUG": 20,
    "INFO": 30,
    "WARN": 40,
    "ERROR": 50,
    "FATAL": 60,
}

DEFAULT_FIELDS = {
    "name",
    "event",
    "filename",
    "func_name",
    "level",
    "lineno",
    "module",
    "pathname",
    "process",
    "qual_name",
    "timestamp",
}


class BunyanFormatter:
    def __init__(self, project_name: str, project_root: Path) -> None:
        self.project_name = project_name
        self.project_root = project_root
        self.hostname = socket.gethostname()

    def __call__(self, _: t.Any, method_name: str, event_dict: EventDict) -> EventDict:
        levelname = event_dict.get("level") or method_name
        levelname = levelname.upper()

        file_path = Path(event_dict["pathname"])
        try:
            relative_path = file_path.relative_to(self.project_root)
        except ValueError:
            relative_path = file_path

        target = event_dict["name"]
        log_entry = {
            "v": 0,
            "name": self.project_name,
            "msg": event_dict["event"],
            "level": LEVEL_MAP.get(levelname, 30),
            "levelname": levelname,
            "hostname": self.hostname,
            "pid": event_dict["process"],
            "time": event_dict["timestamp"],
            "target": target,
            "line": event_dict["lineno"],
            "file": str(relative_path),
        }
        extra_fields = {k: v for k, v in event_dict.items() if k not in DEFAULT_FIELDS}
        if extra_fields:
            log_entry["extra"] = extra_fields
        if "exception" in event_dict:
            log_entry["err"] = self._format_exception(event_dict)
        return log_entry

    def _format_exception(self, event_dict: EventDict) -> EventDict:
        print(f"{event_dict=}")
        return event_dict["exception"]


def configure_telemetry(config: TelemetryConfig) -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.dict_tracebacks,
            structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%S.%fZ", utc=True),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.PROCESS,
                    structlog.processors.CallsiteParameter.QUAL_NAME,
                ]
            ),
            BunyanFormatter(project_name=config.project_name, project_root=config.project_root),
            structlog.processors.JSONRenderer(serializer=jsonlib.dumps),
        ],
        logger_factory=structlog.BytesLoggerFactory(file=sys.stderr.buffer),
    )
    # resource = Resource.create(attributes={SERVICE_NAME: config.project_name})
    # # _init_otel_logging(config, resource)

    # tracer_provider = TracerProvider(resource=resource)
    # processor = BatchSpanProcessor(ConsoleSpanExporter(out=sys.stderr))
    # tracer_provider.add_span_processor(processor)
    # trace.set_tracer_provider(tracer_provider)

    # LoggingInstrumentor().instrument(tracer_provider=tracer_provider, set_logging_format=False)
    # configure_logging(config)
    # reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    # meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    # metrics.set_meter_provider(meter_provider)


# def _init_otel_logging(config: TelemetryConfig, resource: Resource) -> None:
#     log_level = getattr(logging, config.level.upper())

#     logger_provider = LoggerProvider(resource=resource)


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
