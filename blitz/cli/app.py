# from .commands.swagger import list_routes
import typer

from .commands.create import create_blitz_app
from .commands.list import list_blitz_app
from .commands.release import release_blitz
from .commands.start import start_blitz
from .commands.swagger import list_routes

app = typer.Typer()
app.command(name="create")(create_blitz_app)
app.command(name="list")(list_blitz_app)
app.command(name="start")(start_blitz)
app.command(name="release")(release_blitz)
app.command(name="swagger")(list_routes)
# dev only
# app.command(name="clean")(clean_blitz)
