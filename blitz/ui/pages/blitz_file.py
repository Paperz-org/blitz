from blitz.ui.components.json_editor import BlitzFileEditorComponent

from blitz.ui.pages.base import BasePage


class BlitzFilePage(BasePage):
    PAGE_NAME = "Blitz File"

    def render(self) -> None:
        if self.blitz_ui.current_app is None:
            # TODO handle error
            raise Exception
        BlitzFileEditorComponent(self.blitz_ui.current_app.file.raw_file).render()
