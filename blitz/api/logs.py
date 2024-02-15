from loguru import logger
import logging
import inspect
import sys
from typing import TYPE_CHECKING

from blitz.app import BlitzApp

if TYPE_CHECKING:
    from blitz.api.blitz_api import BlitzAPI


class InterceptHandler(logging.Handler):
    def __init__(self, level: int = logging.NOTSET) -> None:
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        if record.name in ("uvicorn.access",):
            if record.args[2].startswith("/projects"):  # type: ignore
                record.name += ".ui"
            elif record.args[2].startswith("/api"):  # type: ignore
                record.name += ".api"
            elif record.args[2].startswith("/admin"):  # type: ignore
                record.name += ".admin"

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1
        if record.name in ["uvicorn.access.ui", "uvicorn.access.admin"]:
            pass
        else:
            logger.opt(
                depth=depth,
                exception=record.exc_info,
            ).log(level, record.getMessage())


def filter_logs(record: logging.LogRecord, blitz_app: BlitzApp) -> bool:
    if record["name"].startswith("uvicorn.access"):  # type: ignore
        return True
    if record["name"].startswith("uvicorn.server"):  # type: ignore
        return True
    if record["name"].startswith("uvicorn.lifespan"):  # type: ignore
        return True
    if record["name"].startswith("uvicorn.error"):  # type: ignore
        return True
    if record["name"].startswith("uvicorn.asgi"):  # type: ignore
        return True
    if record["name"].startswith("uvicorn.protocols"):  # type: ignore
        return True
    if record["extra"].get("blitz_app", "") == blitz_app.name:  # type: ignore
        return True
    return False


def configure(app: "BlitzAPI") -> None:
    logger.remove()
    logger.bind(app_name=app.blitz_app.name)
    logger.add(
        sys.stderr,
        format=("<level>{level: <9}</level>" f" {app.blitz_app.name} " "{message}"),
        colorize=True,
        filter=lambda record: filter_logs(record, app.blitz_app),  # type: ignore
    )
    logger.level("INFO", color="<cyan><bold>")
    logger.level("DEBUG", color="<white><bold>")
    logger.level("ERROR", color="<red><bold>")
    logger.level("WARNING", color="<yellow><bold>")

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
