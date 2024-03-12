import logging

from nicegui import ui

from blitz.api.logs import InterceptHandler
from blitz.ui.components.base import BaseComponent


class LogComponent(BaseComponent[ui.log]):
    class LogHandler(InterceptHandler):
        ANONYMISED_MESSAGE = "[ANONYMISED] *****"

        """A logging handler that emits messages to a log element."""

        def __init__(self, log: ui.log, level: int = logging.NOTSET, is_anonymised: bool = False) -> None:
            self.log = log
            self._is_anonymised = is_anonymised
            super().__init__(level)

        def emit(self, record: logging.LogRecord) -> None:
            try:
                if record.name != "uvicorn.access.ui":
                    message = record.getMessage() if not self._is_anonymised else self.ANONYMISED_MESSAGE
                    self.log.push(message)
            except Exception:
                self.handleError(record)

    def __init__(self) -> None:
        self._logger = logging.getLogger("uvicorn.access")
        self._anonymize_log = self.blitz_ui.read_only
        super().__init__()

    def render(self) -> None:
        self.ng = ui.log(max_lines=None).classes("w-full h-64 text-sm")
        self._logger.addHandler(self.LogHandler(self.ng, is_anonymised=self._anonymize_log))
