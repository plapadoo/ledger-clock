#!/usr/bin/env bash

ledgerclock=./result/bin/ledgerclock

set -e

$ledgerclock --commit-clocks

notify-send "Clocks commited"
