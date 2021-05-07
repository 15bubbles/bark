import os
import platform
import typing

from commands import (
    AddBookmarkCommand,
    DeleteBookmarkCommand,
    ListBookmarksCommand,
    QuitCommand,
)
from options import Option

OptionsMapping = typing.Dict[str, Option]


def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_options(options: OptionsMapping) -> None:
    for key, option in options.items():
        print(f"({key}): {option.name}")


if __name__ == "__main__":
    options = {
        "A": Option("Add new bookmark", AddBookmarkCommand()),
        "B": Option(
            "List bookmarks by creation date",
            # TODO: perhaps this is a bit of an abstraction leak, that we need to know fields on this level
            ListBookmarksCommand(order_by="date_added"),
        ),
        "T": Option(
            "List bookmarks by title",
            # TODO: perhaps this is a bit of an abstraction leak, that we need to know fields on this level
            ListBookmarksCommand(order_by="title"),
        ),
        "D": Option("Delete bookmark", DeleteBookmarkCommand()),
        "Q": Option("Quit", QuitCommand()),
    }

    print("Hello to Bark!")
    print_options(options)
