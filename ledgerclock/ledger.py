from pathlib import Path
from datetime import date, timedelta
from typing import List, NamedTuple, Iterable
from fuzzyfinder import fuzzyfinder


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
    with filename.open() as f:
        account_lines = (line for line in f
                         if line.upper().startswith('ACCOUNT '))
        return [Account(line[8:]) for line in account_lines]


def fuzzy_search(accounts: List[Account], needle: str) -> List[Account]:
    return (Account(result) for result in list(
        fuzzyfinder(needle, [acc.content for acc in accounts])))


def add_entry(filename: Path, entries: Iterable[LedgerEntry]) -> None:
    accounts = get_accounts(filename)
    with filename.open('a') as f:
        for entry in entries:
            f.write('\n')
            f.write('{} {}  ; {}\n'.format(entry.date.isoformat(), entry.payee,
                                           entry.comment))
            f.write('\t{}  {:.2f}h  ; :{}:\n'.format(
                entry.account,
                entry.hours.total_seconds() / 3600, entry.user))
            quota = entry.account.replace('usage', 'quota')
            while not quota in accounts and ':' in quota:
                quota = quota[:quota.rfind(':')]
            f.write('\t{}\n'.format(quota))


def add_account(filename: Path, name: str) -> None:
    pass
