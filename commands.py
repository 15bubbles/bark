import abc
import datetime
import sys
from dataclasses import asdict, dataclass
from typing import Any, Callable, List, Optional, TypedDict

from db import DBInteractor


# CONSTANTS

DB = DBInteractor("bookmarks.db")
TABLE_NAME = "bookmarks"


# TYPE DEFINITIONS


# TODO: perhaps could fiddle with some generic as result(?)
@dataclass(frozen=True)
class Bookmark:
    id: int
    title: str
    url: str
    notes: str = ""


@dataclass(frozen=True)
class CommandResult:
    success: bool
    result: Any
    callback: Optional[Callable] = None

    def __post_init__(self):
        if callable(self.callback) is True:
            self.callback()


@dataclass(frozen=True)
class AddBookmarkData:
    title: str
    url: str
    notes: str


@dataclass(frozen=True)
class DeleteBookmarkData:
    id: int


# COMMANDS


# TODO: perhaps some generics, or just rely on dictionary when pushing data to a command?
class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: Any) -> CommandResult:
        pass


class CreateTableCommand(Command):
    def execute(self, data=None) -> CommandResult:
        DB.create_db(
            TABLE_NAME,
            {
                "id": "integer autoincrement primary key",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )

        return CommandResult(True, None)


class AddBookmarkCommand(Command):
    def execute(self, data: AddBookmarkData) -> CommandResult:
        DB.create_db(
            TABLE_NAME,
            {
                **asdict(data),
                "date_added": datetime.datetime.utcnow().isoformat(),
            },
        )

        return CommandResult(True, None)


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str):
        self.order_by = order_by

    def execute(self, data=None) -> CommandResult:
        bookmarks = DB.get(TABLE_NAME, order_by=self.order_by).fetchall()

        return CommandResult(True, bookmarks)


class DeleteBookmarkCommand(Command):
    def execute(self, data: DeleteBookmarkData) -> CommandResult:
        DB.delete(TABLE_NAME, asdict(data))

        return CommandResult(True, None)


# TODO: not sure if approach with passing callback to `QuitCommand` is proper approach?
# perhaps quitting the program should be a responsibility of presentation layer?
class QuitCommand(Command):
    def execute(self, data=None) -> CommandResult:
        return CommandResult(True, None, sys.exit)
