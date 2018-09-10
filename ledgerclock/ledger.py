from pathlib import Path
from datetime import date, timedelta
from typing import List, NamedTuple, Iterable
from fuzzyfinder import fuzzyfinder  # type: ignore


class Account(NamedTuple):
    content: str


class LedgerEntry(NamedTuple):
    account: Account
    tag: str
    date: date  # type: ignore
    hours: timedelta
    comment: str
    payee: str


def get_granularity(filename: Path) -> timedelta:
    with filename.open() as f:
        granu_lines = [
            line for line in f
            if line.upper().startswith('; #PRAGMA GRANULARITY=')
        ]
        granularity = int(granu_lines[0].split('=')[-1]) if granu_lines else 15
        return timedelta(minutes=granularity)


def get_accounts(filename: Path) -> List[Account]:
    with filename.open() as f:
        account_lines = (line for line in f
                         if line.upper().startswith('ACCOUNT '))
        return [Account(line[8:].rstrip()) for line in account_lines]


def fuzzy_search(accounts: List[Account], needle: str) -> Iterable[Account]:
    return (Account(result) for result in list(
        fuzzyfinder(needle, [acc.content for acc in accounts])))


def add_entries(filename: Path, entries: List[LedgerEntry]) -> None:
    accounts = get_accounts(filename)
    accounts_to_add = [
        entry.account.content for entry in entries
        if not entry.account in accounts
    ]
    if accounts_to_add:
        add_accounts(filename, accounts_to_add)
    with filename.open('a') as f:
        for entry in entries:
            f.write('\n')
            f.write('{} {}  ; {}\n'.format(entry.date.isoformat(), entry.payee,
                                           entry.comment))
            f.write('\t{}  {:.2f}h  ; :{}:\n'.format(
                entry.account.content,
                entry.hours.total_seconds() / 3600, entry.tag))
            quota = entry.account.content.replace('usage', 'quota')
            while not Account(quota) in accounts and ':' in quota:
                quota = quota[:quota.rfind(':')]
            f.write('\t{}\n'.format(quota))


def add_accounts(filename: Path, names: Iterable[str]) -> None:
    with filename.open('r+') as f:
        lines = f.readlines()
        indices = [
            idx for (idx, l) in enumerate(lines)
            if l.upper().startswith('ACCOUNT ')
        ]
        index = max(indices if indices else [len(lines) - 1])
        for (offset, name) in enumerate(names):
            lines.insert(index + offset + 1, 'account {}\n'.format(
                name.replace('usage', 'quota')))
            lines.insert(index + offset + 1, 'account {}\n'.format(name))
        f.seek(0)
        f.write("".join(lines))
