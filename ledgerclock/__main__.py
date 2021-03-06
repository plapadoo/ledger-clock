import argparse
from pathlib import Path
from ledgerclock.ledger import get_accounts, get_payees
from ledgerclock.config_file import read_config_file
from ledgerclock.buffer_file import (start_clock, stop_clock, recent_comments,
                                     commit_clocks, get_active_clock)


# pylint: disable=too-many-branches
def main() -> None:
    parser = argparse.ArgumentParser(description='ledgerclock')
    parser.add_argument(
        '--list-files',
        action='store_true',
        help='list all ledger files',
    )
    parser.add_argument(
        '--list-accounts',
        action='store_true',
        help='list accounts in given ledger file',
    )
    parser.add_argument(
        '--list-recent-comments',
        action='store_true',
        help='list recent comments in given ledger file for a given account',
    )
    parser.add_argument(
        '--list-payees',
        action='store_true',
        help='list payees in given ledger file',
    )
    parser.add_argument(
        '--stop-clock',
        action='store_true',
        help='stop the current clock',
    )
    parser.add_argument(
        '--start-clock',
        action='store_true',
        help='start the given clock',
    )
    parser.add_argument(
        '--get-active-clock',
        action='store_true',
        help='get the name of the active clock (account)',
    )
    parser.add_argument(
        '--commit-clocks',
        action='store_true',
        help='commit all clocks',
    )
    parser.add_argument(
        '--ledger-file',
        action='store',
        type=str,
        nargs='?',
        help='ledger file to consider',
    )
    parser.add_argument(
        '--account',
        action='store',
        type=str,
        nargs='?',
        help='account to consider',
    )
    parser.add_argument(
        '--comment',
        action='store',
        type=str,
        nargs='?',
        help='comment for the work',
    )
    parser.add_argument(
        '--payee',
        action='store',
        type=str,
        nargs='?',
        help='payee to consider',
    )
    args = parser.parse_args()
    if args.start_clock:
        start_clock(
            Path(args.ledger_file),
            args.account,
            args.comment,
            args.payee,
        )
    if args.commit_clocks:
        commit_clocks()
    if args.stop_clock:
        stop_clock()
    if args.get_active_clock:
        ac = get_active_clock()
        if ac is not None:
            print(ac[0].account + " (" + ac[1] + ")")
    if args.list_accounts:
        for a in get_accounts(Path(args.ledger_file)):
            print(a)
    if args.list_payees:
        for a in get_payees(Path(args.ledger_file)):
            print(a)
    if args.list_recent_comments:
        for a in recent_comments(Path(args.ledger_file), args.account):
            print(a)
    if args.list_files:
        for lf in read_config_file().ledger_files:
            print(lf)
