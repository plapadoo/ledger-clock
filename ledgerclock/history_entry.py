from typing import NamedTuple, Any, Dict
from pathlib import Path


class HistoryEntry(NamedTuple):
    filename: Path
    account: str
    comment: str


def history_entry_to_json(h: HistoryEntry) -> Dict[str, Any]:
    return {
        'filename': str(h.filename),
        'account': h.account,
        'comment': h.comment
    }


def history_entry_from_json(h: Dict[str, Any]) -> HistoryEntry:
    return HistoryEntry(
        filename=Path(h['filename']),
        account=h['account'],
        comment=h['comment'],
    )
