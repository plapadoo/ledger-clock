#!/usr/bin/env bash

ledgerclock=./result/bin/ledgerclock

[ -x "$(command -v notify-send)" ] || die "couldn't find notify-send"

ac="$("$ledgerclock" --get-active-clock)"

if [ -z "$ac" ]; then
    notify-send "No active clock, stopping nothing"
else 
    "$ledgerclock" --stop-clock

    notify-send "clock “$ac” stopped"
fi 
