#!/usr/bin/env bash

ledgerclock_bin=ledgerclock

[ -x "$(command -v notify-send)" ] || die "couldn't find notify-send"

ac="$("$ledgerclock_bin" --get-active-clock)"

if [ -z "$ac" ]; then
    notify-send "No active clock, stopping nothing"
else 
    "$ledgerclock_bin" --stop-clock

    notify-send "clock “$ac” stopped"
fi 
