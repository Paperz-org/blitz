from nicegui import ui

from blitz.ui.pages.base import BasePage


class SwaggerPage(BasePage):
    PAGE_NAME = "Swagger"

    def resize_iframe(self) -> None:
        ui.run_javascript(
            """
            var iframe = document.querySelector('iframe');
            var resizeIframe = function() {
                iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
            };
            
            """
        )

    def render(self) -> None:
        self.resize_iframe()

        ui.element("iframe").props(
            f"src={self.blitz_ui.localhost_url}/api/docs frameborder=0 onload=resizeIframe()"
        ).classes("w-full rounded-sm bg-white h-screen overflow-hidden")
