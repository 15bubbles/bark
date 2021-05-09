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
# NOTE: perhaps creation of database should not be done in init
# NOTE: most probably database interactor instance should be injected
# from above to simplify testing (?)
class SQLiteBookmarksRepository(BookmarksRepository):
    def __init__(
        self,
        db_filename: str = "../bookmarks.db",
        table_name: str = "bookmarks",
    ):
        self.db_interactor = SQLiteInteractor(db_filename)
        self.table_name = table_name
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
        cursor = self.db_interactor.get(self.table_name, order_by=order_by)
        bookmarks = cursor.fetchall()

        return [Bookmark(**bookmark) for bookmark in bookmarks]

    def get(self, data: GetBookmarkData) -> Union[Bookmark, None]:
        cursor = self.db_interactor.get(
            self.table_name, filters={"id": data.id}
        )
        bookmark = cursor.fetchone()

        if bookmark is None:
            return None

        return Bookmark(**bookmark)

    def delete(self, data: DeleteBookmarkData) -> None:
        self.db_interactor.delete(self.table_name, {"id": data.id})
