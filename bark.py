import os
import platform
import typing

from options import Option


OptionsMapping = typing.Dict[str, Option]


def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_options(options: OptionsMapping) -> None:
    for key, option in options.items():
        print(f"{key}: {option.name}")


if __name__ == "__main__":
    options = {
        "A": Option("Add new bookmark"),
    }

    print_options(options)
