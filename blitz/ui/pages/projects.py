from nicegui import ui

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui


class ProjectDetail:
    def __init__(
        self,
        app_name: str,
        project_name: str = "",
        date: str = "",
        description: str = "",
        version: str = "",
    ) -> None:
        self.app_name=app_name
        self.project_name = project_name
        self.date = date
        self.description = description
        self.version = version


    def render(self):
        with ui.link(target=f"/projects/{self.app_name}").classes("w-full hover:bg-slate-700 rounded-sm"), ui.grid(
            columns=20
        ).classes("w-full my-2"):
            ui.label(self.app_name).classes("col-span-2 pl-2")
            ui.label(self.project_name).classes("col-span-2 pl-2")
            ui.label(self.date).classes("col-span-4")
            ui.label(self.description).classes("col-span-11")
            ui.label(self.version).classes("col-span-1")


class HomePage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui

    def render_page(self):
        with ui.element("div").classes(
            "w-full justify-center items-center content-center p-10"
        ):
            with ui.card().classes("no-shadow border align-center"):
                with ui.row().classes("w-full justify-between items-center"):
                    ui.label("Blitz Projects").classes("text-2xl")
                    with ui.button("New").props("disabled").props("flat"):
                        ui.tooltip(
                            "This feature is not developed yet. Create a new project with the CLI."
                        )
                ui.input(label="Search for project").props(
                    "borderless standout dense"
                ).classes(" rounded-lg px-2 border-solid border w-full my-5")
                with ui.grid(columns=20).classes("w-full"):
                    ui.label("App").classes("col-span-2 pl-2")
                    ui.label("Name").classes("col-span-2 pl-2")
                    ui.label("Last modified").classes("col-span-4")
                    ui.label("Description").classes("col-span-11")
                    ui.label("Version").classes("col-span-1")

                ui.separator()

                for app in self.blitz_ui.apps:
                    ProjectDetail(app_name=app.name, project_name=app.file.config.name, description=app.file.config.description,version=app.file.config.version).render()
