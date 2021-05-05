from typing import Any, Callable, Optional

from commands import Command


class Option:
    def __init__(
        self,
        name: str,
        command: Command,
        preparation_callback: Optional[Callable[[], Any]] = None,
    ):
        self.name = name
        self.command = command
        self.preparation_callback = preparation_callback

    def __repr__(self) -> str:
        return f"Option({self.name!r}, {self.command!r}, {self.preparation_callback!r})"

    def __str__(self) -> str:
        return self.name

    def choose(self) -> None:
        data = (
            self.preparation_callback()
            if self.preparation_callback is not None
            else None
        )
        message = (
            self.command.execute(data)
            if data is not None
            else self.command.execute()
        )

        print(message)
