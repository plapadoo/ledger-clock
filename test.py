import time
from pathlib import Path
from ledgerclock.buffer_file import start_clock, stop_clock, commit_clocks

start_clock(Path("/tmp/foo.ledger"), "foo:usage:bar", "mycomment", "mypayee")
time.sleep(2)
stop_clock()
commit_clocks()
