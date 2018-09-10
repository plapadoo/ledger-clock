from typing import List
from pathlib import Path
from ledgerclock.buffer_entry import BufferEntry


class BufferFile:
    def __init__(
            self,
            entries: List[BufferEntry],
    ) -> None:
        pass


def start_clock(
        filename: Path,
        account: str,
        comment: str,
        payee: str,
) -> None:
    pass


def stop_clock() -> None:
    pass


def commit_clocks() -> None:
    pass
