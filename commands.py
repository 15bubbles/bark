import datetime
import sys
from dataclasses import asdict, dataclass
from typing import List

from db import DBInteractor


# CONSTANTS

DB = DBInteractor("bookmarks.db")
TABLE_NAME = "bookmarks"


# TYPE DEFINITIONS


@dataclass(frozen=True)
class AddBookmarkData:
    title: str
    url: str
    notes: str


@dataclass(frozen=True)
class DeleteBookmarkData:
    id: int


# COMMANDS


class CreateTableCommand:
    def execute(self) -> str:
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
        return f"Table {TABLE_NAME} created!"


class AddBookmarkCommand:
    def execute(self, data: AddBookmarkData) -> str:
        DB.create_db(
            TABLE_NAME,
            {
                **asdict(data),
                "date_added": datetime.datetime.utcnow().isoformat(),
            },
        )
        return "Bookmark created!"


class ListBookmarksCommand:
    def __init__(self, order_by: str):
        self.order_by = order_by

    def execute(self) -> List[str]:
        return DB.get(TABLE_NAME).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data: DeleteBookmarkData) -> str:
        DB.delete(TABLE_NAME, asdict(data))
        return "Bookmark deleted!"


class QuitCommand:
    def execute(self):
        sys.exit()
