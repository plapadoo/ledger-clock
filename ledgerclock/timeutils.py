import datetime
import time


def iso_str_to_datetime(s: str) -> datetime:
    return datetime.datetime(*time.strptime(s, "%Y-%m-%dT%H:%M:%S")[:6])
