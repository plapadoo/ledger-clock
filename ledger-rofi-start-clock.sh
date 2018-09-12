#!/usr/bin/env bash

ledgerclock_bin=ledgerclock

set -e 

function die() {
    echo "$@"
    exit 1
}

[ -x "$(command -v rofi)" ] || die "couldn't find rofi"
[ -x "$(command -v notify-send)" ] || die "couldn't find notify-send"

selected_file="$($ledgerclock_bin --list-files | rofi -dmenu -matching fuzzy -p ledger -no-custom)"

[[ -n "$selected_file" ]] || exit 1

selected_account="$($ledgerclock_bin --list-accounts --ledger-file "$selected_file" | rofi -dmenu -matching fuzzy -p account)"

[[ -n "$selected_account" ]] || exit 2

selected_payee="$($ledgerclock_bin --list-payees --ledger-file "$selected_file" | rofi -dmenu -matching fuzzy -p payee)"

[[ -n "$selected_payee" ]] || exit 3

comment="$($ledgerclock_bin --list-recent-comments --ledger-file "$selected_file" --account "$selected_account" | rofi -dmenu -p comment)"

ac="$("$ledgerclock_bin" --get-active-clock)"

$ledgerclock_bin \
    --ledger-file "$selected_file"\
    --account "$selected_account"\
    --comment "$comment"\
    --payee "$selected_payee"\
    --start-clock

if [ -z "$ac" ]; then
    notify-send "Clock for “$selected_account” started"
else
    notify-send "Switched from “$ac” to “$selected_account”"
fi
