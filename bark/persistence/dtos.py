from dataclasses import dataclass


@dataclass(frozen=True)
class Bookmark:
    id: str
    title: str
    url: str
    notes: str
    date_added: str


@dataclass(frozen=True)
class AddBookmarkData:
    title: str
    url: str
    notes: str = ""


@dataclass(frozen=True)
class EditBookmarkData:
    id: str
    title: str
    url: str
    notes: str


@dataclass(frozen=True)
class GetBookmarkData:
    id: str


@dataclass(frozen=True)
class DeleteBookmarkData:
    id: str
