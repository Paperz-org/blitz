from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.json_editor import BlitzFileEditorComponent


class BlitzFilePage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui(), project: str | None = None) -> None:
        self.blitz_ui = blitz_ui
        self.blitz_app = blitz_ui.current_app

    def render_page(self) -> None:
        if self.blitz_app is None:
            # TODO handle error
            raise Exception
        BlitzFileEditorComponent(self.blitz_app.file.raw_file).render()
