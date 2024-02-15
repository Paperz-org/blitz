import typer

from typing import Annotated


def compile_blitz(filename: Annotated[str, typer.Argument()]) -> None:
    print(f"{filename}")
