import logging
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from nicegui import ui
from blitz.api.logs import InterceptHandler
from blitz.ui.components.base import BaseComponent


class LogComponent(BaseComponent[ui.log]):
    class LogHandler(InterceptHandler):
        """A logging handler that emits messages to a log element."""

        def __init__(self, log: ui.log, level: int = logging.NOTSET) -> None:
            self.log = log
            super().__init__(level)

        def emit(self, record: logging.LogRecord) -> None:
            try:
                if record.name != "uvicorn.access.ui":
                    self.log.push(record.getMessage())
            except Exception:
                self.handleError(record)

    def __init__(self) -> None:
        self._logger = logging.getLogger("uvicorn.access")
        super().__init__()

    def render(self) -> None:
        self.ng = ui.log(max_lines=None).classes("w-full h-64 text-sm")
        self._logger.addHandler(self.LogHandler(self.ng))
