#!/usr/bin/env bash

ledgerclock=./result/bin/ledgerclock

set -e 

function die() {
    echo "$@"
    exit 1
}

[ -x "$(command -v rofi)" ] || die "couldn't find rofi"
[ -x "$(command -v notify-send)" ] || die "couldn't find notify-send"

selected_file="$($ledgerclock --list-files | rofi -dmenu -matching fuzzy -p ledger -no-custom)"

[[ -n "$selected_file" ]] || exit 1

selected_account="$($ledgerclock --list-accounts --ledger-file "$selected_file" | rofi -dmenu -matching fuzzy -p account)"

[[ -n "$selected_account" ]] || exit 2

selected_payee="$($ledgerclock --list-payees --ledger-file "$selected_file" | rofi -dmenu -matching fuzzy -p payee)"

[[ -n "$selected_payee" ]] || exit 3

comment="$($ledgerclock --list-recent-comments --ledger-file "$selected_file" --account "$selected_account" | rofi -dmenu -p comment)"

ac="$("$ledgerclock" --get-active-clock)"

$ledgerclock \
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
