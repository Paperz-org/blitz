from nicegui import ui


from blitz.ui.components.base import BaseComponent


class BaseMarkdown(BaseComponent[ui.markdown], reactive=True):
    def __init__(
        self,
        content: str = "",
        extras: list[str] = ["fenced-code-blocks", "tables"],
        classes: str = "",
        props: str = "",
    ) -> None:
        self.content = content
        self.extras = extras
        super().__init__(classes=classes, props=props)

    def render(self) -> None:
        self.ng = ui.markdown(content=self.content, extras=self.extras).props(self.props).classes(self.classes)


class MarkdownResponse(BaseMarkdown, render=False):
    """Don't render by default"""
