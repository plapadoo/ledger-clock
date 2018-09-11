#!/usr/bin/env bash

ledgerclock=./result/bin/ledgerclock

[ -x "$(command -v notify-send)" ] || die "couldn't find notify-send"

set -e

$ledgerclock --commit-clocks

notify-send "Clocks commited"
