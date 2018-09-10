from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from itertools import groupby
import json
from datetime import datetime
from xdg.BaseDirectory import save_data_path
from ledgerclock.timeutils import iso_str_to_datetime
from ledgerclock.buffer_entry import BufferEntry
from ledgerclock.ledger import add_entries, LedgerEntry, Account
from ledgerclock.config_file import read_config_file


class BufferFile:
    def __init__(
            self,
            open_entry: Optional[BufferEntry],
            entries: List[BufferEntry],
    ) -> None:
        self.open_entry = open_entry
        self.entries = entries


def entry_from_json(e: Dict[str, Any]) -> BufferEntry:
    return BufferEntry(
        filename=Path(e['filename']),
        account=e['account'],
        start=iso_str_to_datetime(e['start']),
        end=iso_str_to_datetime(e['end']) if 'end' in e else None,
        comment=e['comment'],
        payee=e['payee'],
    )


def entry_to_json(b: BufferEntry) -> Dict[str, Any]:
    result = {
        'filename': str(b.filename),
        'account': b.account,
        'start': b.start.isoformat(timespec='seconds'),
        'comment': b.comment,
        'payee': b.payee,
    }
    if b.end is not None:
        result['end'] = b.end.isoformat(timespec='seconds')
    return result


def buffer_file() -> Path:
    return Path(save_data_path("ledgerclock")) / "data.json"


def file_from_json(json_obj: Dict[str, Any]) -> BufferFile:
    entries = [entry_from_json(e) for e in json_obj['entries']]
    open_entry = entry_from_json(
        json_obj['open_entry']
    ) if 'open_entry' in json_obj and json_obj['open_entry'] is not None else None
    return BufferFile(open_entry=open_entry, entries=entries)


def file_to_json(b: BufferFile) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    if b.open_entry is not None:
        result['open_entry'] = entry_to_json(b.open_entry)
    result['entries'] = []
    for e in b.entries:
        result['entries'].append(entry_to_json(e))
    return result


def read_buffer_file() -> BufferFile:
    path = buffer_file()
    if not path.exists():
        return BufferFile(open_entry=None, entries=[])
    with path.open() as f:
        return file_from_json(json.load(f))


def write_buffer_file(f: BufferFile) -> None:
    buffer_file().write_text(json.dumps(file_to_json(f), indent=2))


def start_clock(
        filename: Path,
        account: str,
        comment: str,
        payee: str,
) -> None:
    bf = read_buffer_file()
    if bf.open_entry is not None:
        stop_clock()
        bf = read_buffer_file()
    now = datetime.utcnow()
    bf.open_entry = BufferEntry(
        filename=filename,
        account=account,
        comment=comment,
        payee=payee,
        start=now,
        end=None,
    )
    write_buffer_file(bf)


def stop_clock() -> None:
    now = datetime.utcnow()
    f = read_buffer_file()
    if f.open_entry is None:
        raise Exception('no open clock present')
    f.open_entry.end = now
    f.entries.append(f.open_entry)
    f.open_entry = None
    write_buffer_file(f)


def compare_entries(e: BufferEntry) -> Tuple[Path, str, str, str]:
    return (e.filename, e.account, e.comment, e.payee)


def to_ledger_entry(e: BufferEntry) -> LedgerEntry:
    if e.end is None:
        raise Exception('cannot ledgerify entry with no end time')
    return LedgerEntry(
        account=Account(e.account),
        tag=read_config_file().tag,
        date=e.start.date(),
        hours=e.end - e.start,
        comment=e.comment,
        payee=e.payee,
    )


def commit_clocks() -> None:
    bf = read_buffer_file()
    for key, els in groupby(bf.entries, key=compare_entries):
        add_entries(key[0], (to_ledger_entry(e) for e in els))
