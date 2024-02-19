from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui


class BaseComponent:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui: BlitzUI = blitz_ui
        self.current_project = blitz_ui.current_project
        self.current_app = blitz_ui.current_app
