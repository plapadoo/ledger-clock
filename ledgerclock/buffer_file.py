from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from itertools import groupby
import json
from datetime import datetime
from xdg.BaseDirectory import save_data_path  # type: ignore
from ledgerclock.buffer_entry import (BufferEntry, buffer_entry_from_json,
                                      buffer_entry_to_json)
from ledgerclock.ledger import add_entries, LedgerEntry
from ledgerclock.config_file import read_config_file
from ledgerclock.history_entry import (HistoryEntry, history_entry_from_json,
                                       history_entry_to_json)


class BufferFile:
    def __init__(
            self,
            open_entry: Optional[BufferEntry],
            entries: List[BufferEntry],
            history: List[HistoryEntry],
    ) -> None:
        self.open_entry = open_entry
        self.entries = entries
        self.history = history


def _buffer_file() -> Path:
    return Path(save_data_path("ledgerclock")) / "data.json"


def _file_from_json(json_obj: Dict[str, Any]) -> BufferFile:
    open_entry = buffer_entry_from_json(
        json_obj['open_entry']
    ) if 'open_entry' in json_obj and json_obj['open_entry'] is not None else None
    return BufferFile(
        open_entry=open_entry,
        entries=[buffer_entry_from_json(e) for e in json_obj['entries']],
        history=[history_entry_from_json(e) for e in json_obj['history']],
    )


def _file_to_json(b: BufferFile) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    if b.open_entry is not None:
        result['open_entry'] = buffer_entry_to_json(b.open_entry)
    result['history'] = [history_entry_to_json(e) for e in b.history]
    result['entries'] = [buffer_entry_to_json(e) for e in b.entries]
    return result


def _read_buffer_file() -> BufferFile:
    path = _buffer_file()
    if not path.exists():
        return BufferFile(open_entry=None, entries=[], history=[])
    with path.open() as f:
        return _file_from_json(json.load(f))


def _write_buffer_file(f: BufferFile) -> None:
    _buffer_file().write_text(json.dumps(_file_to_json(f), indent=2))


def get_active_clock() -> Optional[Tuple[BufferEntry, str]]:
    e = _read_buffer_file().open_entry
    if e is None:
        return None
    now = datetime.utcnow()
    diff = str(int((now - e.start).total_seconds() / 60)) + "min"
    return (e, diff)


def start_clock(
        filename: Path,
        account: str,
        comment: str,
        payee: str,
) -> None:
    bf = _read_buffer_file()
    if bf.open_entry is not None:
        stop_clock()
        bf = _read_buffer_file()
    now = datetime.utcnow()
    bf.open_entry = BufferEntry(
        filename=filename,
        account=account,
        comment=comment,
        payee=payee,
        start=now,
        end=None,
    )
    bf.history.append(
        HistoryEntry(
            filename=filename,
            account=account,
            comment=comment,
        ))
    _write_buffer_file(bf)


def recent_comments(f: Path, account: str) -> List[str]:
    bf = _read_buffer_file()
    return [
        e.comment for e in bf.history
        if e.filename == f and e.account == account
    ]


def stop_clock() -> None:
    now = datetime.utcnow()
    f = _read_buffer_file()
    if f.open_entry is None:
        raise Exception('no open clock present')
    f.open_entry.end = now
    f.entries.append(f.open_entry)
    f.open_entry = None
    _write_buffer_file(f)


def _compare_entries(e: BufferEntry) -> Tuple[Path, str, str, str]:
    return (e.filename, e.account, e.comment, e.payee)


def _to_ledger_entry(e: BufferEntry) -> LedgerEntry:
    if e.end is None:
        raise Exception('cannot ledgerify entry with no end time')
    return LedgerEntry(
        account=e.account,
        tag=read_config_file().tag,
        date=e.start.date(),
        hours=e.end - e.start,
        comment=e.comment,
        payee=e.payee,
    )


def commit_clocks() -> None:
    bf = _read_buffer_file()
    for key, els in groupby(bf.entries, key=_compare_entries):
        add_entries(key[0], [_to_ledger_entry(e) for e in els])
    bf.entries.clear()
    _write_buffer_file(bf)
