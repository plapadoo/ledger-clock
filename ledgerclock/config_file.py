from typing import NamedTuple, Optional, List, Optional, Any, Dict
from pathlib import Path
import json
from xdg.BaseDirectory import xdg_config_home


class ConfigFile(NamedTuple):
    ledger_files: List[Path]


def read_config_file() -> Optional[ConfigFile]:
    config_path = Path(xdg_config_home) / "ledgerclock" / "config.json"
    if not config_path.exists():
        return None
    with config_path.open() as f:
        json_obj: Dict[str, Any] = json.load(f)
        return ConfigFile(ledger_files=json_obj['ledger_files'])
