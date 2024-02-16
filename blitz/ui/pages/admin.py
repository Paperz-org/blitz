from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from nicegui import ui


class AdminPage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui

    def resize_iframe(self) -> None:
        ui.run_javascript(
            """
            var iframe = document.querySelector('iframe');
            var resizeIframe = function() {
                iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
            };
            var navList = iframe.getElementById('navList');
            if (navList) {
                console.log('hello')
                var lastNavItem = navList.lastElementChild;
                if (lastNavItem) {
                    lastNavItem.style.pointerEvents = 'none';
                    lastNavItem.style.color = 'gray'; 
                }
            }   
            };
            """
        )

    def render_page(self) -> None:
        self.resize_iframe()
        ui.element("iframe").props(
            f"src={self.blitz_ui.localhost_url}/admin/ frameborder=0 onload=resizeIframe()"
        ).classes("w-full rounded-sm bg-white h-screen overflow-hidden")
