import abc
import sys
from typing import Any, List, Optional

from bark.persistence.dtos import AddBookmarkData, Bookmark, DeleteBookmarkData
from bark.persistence.repositories import SQLiteBookmarksRepository


REPOSITORY = SQLiteBookmarksRepository()


class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: Any) -> Optional[Any]:
        pass


class AddBookmarkCommand(Command):
    def execute(self, data: AddBookmarkData) -> None:
        REPOSITORY.create(data)


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str):
        self.order_by = order_by

    def execute(self, data=None) -> List[Bookmark]:
        return REPOSITORY.list(self.order_by)


class DeleteBookmarkCommand(Command):
    def execute(self, data: DeleteBookmarkData) -> None:
        REPOSITORY.delete(data)


# TODO: perhaps this should be presentation's layer responsibility?
class QuitCommand(Command):
    def execute(self, data=None) -> None:
        sys.exit(0)
