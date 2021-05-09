import abc
import datetime
from dataclasses import asdict
from typing import List, Union

from .db import SQLiteInteractor
from .dtos import (
    AddBookmarkData,
    EditBookmarkData,
    GetBookmarkData,
    DeleteBookmarkData,
    Bookmark,
)


class BookmarksRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, data: AddBookmarkData) -> None:
        pass

    @abc.abstractmethod
    def update(self, data: EditBookmarkData) -> None:
        pass

    @abc.abstractmethod
    # NOTE: perhaps this method should also take the approach where an
    # object will be passed that defines filtering
    def list(self, order_by: str) -> List[Bookmark]:
        pass

    @abc.abstractmethod
    def get(self, data: GetBookmarkData) -> Union[Bookmark, None]:
        pass

    @abc.abstractmethod
    def delete(self, data: DeleteBookmarkData) -> None:
        pass


# TODO: `db_filename` and `table_name` should be read from config and
# such config should take values from environment variables
# perhaps database location should be less error prone
class SQLiteBookmarksRepository(BookmarksRepository):
    def __init__(
        self,
        db_filename: str = "../bookmarks.db",
        table_name: str = "bookmarks",
    ):
        self.db_interactor = SQLiteInteractor(db_filename)
        self.table_name = table_name
        # TODO: perhaps creation of database should not be done in init
        self.db_interactor.create_db(
            self.table_name,
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )

    def create(self, data: AddBookmarkData) -> None:
        self.db_interactor.add(
            self.table_name,
            {
                **asdict(data),
                "date_added": datetime.datetime.utcnow().isoformat(),
            },
        )

    def update(self, data: EditBookmarkData) -> None:
        raise NotImplemented("Updates are not implemented yet")

    def list(self, order_by: str) -> List[Bookmark]:
        bookmarks = self.db_interactor.get(self.table_name, order_by=order_by)

        return [Bookmark(**bookmark) for bookmark in bookmarks]

    def get(self, data: GetBookmarkData) -> Bookmark:
        bookmark = self.db_interactor.get(
            self.table_name, filters={"id": data.id}
        )

        if bookmark:
            return Bookmark(**bookmark[0])

        return None

    def delete(self, data: DeleteBookmarkData) -> None:
        self.db_interactor.delete(self.table_name, {"id": data.id})
