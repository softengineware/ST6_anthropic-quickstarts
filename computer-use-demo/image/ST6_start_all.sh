#!/bin/bash

set -e

export DISPLAY=:${DISPLAY_NUM}
./ST6_xvfb_startup.sh
./ST6_tint2_startup.sh
./ST6_mutter_startup.sh
./ST6_x11vnc_startup.sh
