import logging
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from nicegui import ui
from blitz.api.logs import InterceptHandler


class LogElementHandler(InterceptHandler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if record.name != "uvicorn.access.ui":
                self.element.push(record.getMessage())
        except Exception:
            self.handleError(record)


class LogComponent:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui
        self._logger = logging.getLogger("uvicorn.access")

    def render(self):
        log = ui.log(max_lines=None).classes("w-full h-64 text-sm")
        self._logger.addHandler(LogElementHandler(log))
