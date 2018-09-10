from typing import Optional
from pathlib import Path
from datetime import datetime


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
