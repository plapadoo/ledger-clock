#!/usr/bin/env bash

ledgerclock_bin=ledgerclock
notify_bin=notify-send

function die() {
    echo "$@"
    exit 1
}

[ -x "$(command -v "$notify_bin")" ] || die "couldn't find notify-send"

set -e

"$ledgerclock_bin" --commit-clocks

"$notify_bin" "Clocks commited"
