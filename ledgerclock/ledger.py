from pathlib import Path
from datetime import date, timedelta
from typing import List, NamedTuple


class Account(NamedTuple):
    content: str


class LedgerEntry(NamedTuple):
    account: Account
    tag: str
    date: date
    hours: timedelta
    comment: str
    payee: str
    user: str


def get_accounts(filename: Path) -> List[Account]:
    pass


def fuzzy_search(accounts: List[Account], needle: str) -> List[Account]:
    pass


def add_entry(filename: Path, entry: LedgerEntry) -> None:
    pass


def add_account(filename: Path, name: str) -> None:
    pass
