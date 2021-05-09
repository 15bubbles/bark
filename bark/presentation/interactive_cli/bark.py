import os
import platform
from typing import Dict, Union

from bark.commands import (
    AddBookmarkCommand,
    AddBookmarkData,
    DeleteBookmarkCommand,
    DeleteBookmarkData,
    ListBookmarksCommand,
    QuitCommand,
)
from bark.presentation.interactive_cli.options import Option


_OptionsMapping = Dict[str, Option]


# NOTE: some url validation would be nice here
# and some type validation as well
def _get_user_input(label: str, required: bool = False) -> Union[str, None]:
    value = input(f"{label}: ") or None

    while required and not value:
        value = input(f"{label}: ") or None

    return value


def _get_add_bookmark_data():
    return AddBookmarkData(
        title=_get_user_input("Title", required=True),
        url=_get_user_input("URL", required=True),
        notes=_get_user_input("Notes", required=False),
    )


def _get_delete_bookmark_data():
    return DeleteBookmarkData(
        id=_get_user_input("ID", required=True),
    )


def _clear_screen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def _print_options(options: _OptionsMapping) -> None:
    for key, option in options.items():
        print(f"({key}): {option.name}")


def _is_option_valid(option_key: str, options: _OptionsMapping) -> bool:
    if option_key in options:
        return True

    return False


# NOTE: might be useful to create a class that will hold logic with
# application loop
def _loop(options: _OptionsMapping):
    while True:
        _clear_screen()
        _print_options(options)
        user_choice = input("Select an option: ")

        if not _is_option_valid(user_choice.upper(), options):
            print(f"Not a valid choice")
            continue

        selected_option = options[user_choice.upper()]
        selected_option.choose()


_OPTIONS = {
    "A": Option(
        "Add new bookmark",
        AddBookmarkCommand(),
        _get_add_bookmark_data,
    ),
    "B": Option(
        "List bookmarks by creation date",
        # NOTE: perhaps this is a bit of an abstraction leak, that
        # we need to know fields on this level
        ListBookmarksCommand(order_by="date_added"),
    ),
    "T": Option(
        "List bookmarks by title",
        # NOTE: perhaps this is a bit of an abstraction leak, that
        # we need to know fields on this level
        ListBookmarksCommand(order_by="title"),
    ),
    "D": Option(
        "Delete bookmark",
        DeleteBookmarkCommand(),
        _get_delete_bookmark_data,
    ),
    "Q": Option(
        "Quit",
        QuitCommand(),
    ),
}


if __name__ == "__main__":
    print("Hello to Bark!")
    _loop(_OPTIONS)
