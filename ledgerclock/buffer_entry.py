from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from ledgerclock.timeutils import iso_str_to_datetime


class BufferEntry:
    def __init__(
            self,
            filename: Path,
            account: str,
            start: datetime,
            end: Optional[datetime],
            comment: str,
            payee: str,
    ) -> None:
        self.filename = filename
        self.account = account
        self.start = start
        self.end = end
        self.comment = comment
        self.payee = payee


def buffer_entry_from_json(e: Dict[str, Any]) -> BufferEntry:
    return BufferEntry(
        filename=Path(e['filename']),
        account=e['account'],
        start=iso_str_to_datetime(e['start']),
        end=iso_str_to_datetime(e['end']) if 'end' in e else None,
        comment=e['comment'],
        payee=e['payee'],
    )


def buffer_entry_to_json(b: BufferEntry) -> Dict[str, Any]:
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
