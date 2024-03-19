from blitz.ui.components.links.menu_link import MenuLink
from .base import BaseLeftDrawer


class DashboardDrawer(BaseLeftDrawer.variant(classes="px-0 bg-[#14151a]", props="width=200")):  # type: ignore
    def __init__(self, drawer_open: bool) -> None:
        super().__init__(value=drawer_open)

    def render(self) -> None:
        super().render()
        with self:
            MenuLink("Dashboard", f"/projects/{self.current_project}", "dashboard")
            MenuLink("Admin", f"{self.blitz_ui.localhost_url}/admin/", "table_chart")
            MenuLink("Swagger", f"/projects/{self.current_project}/swagger", "api")
            MenuLink("Blitz File", f"/projects/{self.current_project}/blitz-file", "article")
            MenuLink("Diagram", f"/projects/{self.current_project}/diagram", "account_tree")
            MenuLink("Logs", f"/projects/{self.current_project}/logs", "list")
            MenuLink("Resources", f"/projects/{self.current_project}/resources", "topic")
