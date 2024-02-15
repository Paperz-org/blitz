import pathlib
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from nicegui import ui
from pathlib import Path


class SwaggerPage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui(), project: str = None) -> None:
        self.blitz_ui = blitz_ui
    
    def resize_iframe(self):
        ui.run_javascript(
            """
            var iframe = document.querySelector('iframe');
            var resizeIframe = function() {
                iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
            };
            
            """)

    def render_page(self):
        self.resize_iframe()
       
        ui.element("iframe").props(
                "src={self.blitz_ui.localhost_url}/api/docs frameborder=0 onload=resizeIframe()"
            ).classes("w-full rounded-sm bg-white h-screen overflow-hidden")
