from typing import Any, Callable, List, Optional, Union

from bark.commands import Command


class Option:
    def __init__(
        self,
        name: str,
        command: Command,
        preparation_callback: Optional[Callable[[], Any]] = None,
        success_message: str = "{result}",
        failure_message: str = "Operation failed",
    ):
        self.name = name
        self.command = command
        self.preparation_callback = preparation_callback
        self.success_message = success_message
        self.failure_message = failure_message

    def __repr__(self) -> str:
        return f"Option({self.name!r}, {self.command!r}, {self.preparation_callback!r})"

    def __str__(self) -> str:
        return self.name

    def _prepare_success_message(self, result: Union[List[Any], Any]) -> str:
        if isinstance(result, list):
            return self.success_message.format(
                "\n".join([str(item) for item in result])
            )

        return self.success_message.format(result)

    def choose(self) -> None:
        data = (
            self.preparation_callback()
            if self.preparation_callback is not None
            else None
        )
        result = self.command.execute(data)
        message = self._prepare_success_message(result)
        print(message)
