#!/usr/bin/env bash

ledgerclock=./result/bin/ledgerclock

"$ledgerclock" --stop-clock

notify-send "clock stopped"
