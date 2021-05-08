import os
import platform
from typing import Dict, Union

from commands import (
    AddBookmarkCommand,
    AddBookmarkData,
    CreateTableCommand,
    DeleteBookmarkCommand,
    DeleteBookmarkData,
    ListBookmarksCommand,
    QuitCommand,
)
from options import Option

OptionsMapping = Dict[str, Option]


# NOTE: some url validation would be nice here
# and some type validation as well
def get_user_input(label: str, required: bool = False) -> Union[str, None]:
    value = input(f"{label}: ") or None

    while required and not value:
        value = input(f"{label}: ") or None

    return value


def get_add_bookmark_data():
    return AddBookmarkData(
        title=get_user_input("Title", required=True),
        url=get_user_input("URL", required=True),
        notes=get_user_input("Notes", required=False),
    )


def get_delete_bookmark_data():
    return DeleteBookmarkData(
        id=get_user_input("ID", required=True),
    )


def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_options(options: OptionsMapping) -> None:
    for key, option in options.items():
        print(f"({key}): {option.name}")


def is_option_valid(option_key: str, options: OptionsMapping) -> bool:
    if option_key in options:
        return True

    return False


def loop(options: OptionsMapping):
    while True:
        clear_screen()
        print_options(options)
        user_choice = input("Select an option: ")

        if not is_option_valid(user_choice.upper(), options):
            print(f"Not a valid choice")
            continue

        selected_option = options[user_choice.upper()]
        result = selected_option.choose()

        if not result.success:
            print("Operation failed")

        if result.success and result.result:
            print(result.result)


if __name__ == "__main__":
    options = {
        "A": Option(
            "Add new bookmark",
            AddBookmarkCommand(),
            get_add_bookmark_data,
        ),
        "B": Option(
            "List bookmarks by creation date",
            # TODO: perhaps this is a bit of an abstraction leak, that
            # we need to know fields on this level
            ListBookmarksCommand(order_by="date_added"),
        ),
        "T": Option(
            "List bookmarks by title",
            # TODO: perhaps this is a bit of an abstraction leak, that
            # we need to know fields on this level
            ListBookmarksCommand(order_by="title"),
        ),
        "D": Option(
            "Delete bookmark",
            DeleteBookmarkCommand(),
            get_delete_bookmark_data,
        ),
        "Q": Option(
            "Quit",
            QuitCommand(),
        ),
    }

    CreateTableCommand().execute()
    print("Hello to Bark!")
    loop(options)
