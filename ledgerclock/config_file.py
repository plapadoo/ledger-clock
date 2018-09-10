from typing import NamedTuple, Optional
from pathlib import Path


class ConfigFile(NamedTuple):
    ledger_files: List[Path]


def read_config_file() -> Optional[ConfigFile]:
    pass
