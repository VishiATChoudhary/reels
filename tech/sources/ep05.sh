#!/usr/bin/env bash
# ep05: Geoffrey Hinton, 60 Minutes (CBS, 2023): "we can't afford to get it wrong with these things."
#   bash tech/sources/ep05.sh
source "$(dirname "$0")/../../tools/lib.sh"
ep tech ep05

# get always takes a section: lib.sh's empty sec array trips set -u on macOS bash 3.2
get hinton  qrvK_KuIeJk 0:00-13:12   # "Godfather of AI" Geoffrey Hinton: The 60 Minutes Interview
get dc      hFbmoms5sD4 0:00-1:33    # royalty free data centre footage
get leds    zce3IGhZL6g 0:00-0:13    # blinking server LEDs
get redsrv  d-NX6iukeSU 0:00-0:16    # server room in red
get h100    QGpniBJiCZw 0:00-1:00    # NVIDIA HGX H100 production run
get code    FTTG0jDdC6A 0:00-1:01    # scrolling code
B=~/shennies/synapse/promo/public/broll
[ -f raw/nnet.mp4 ] || cp "$B/3JQ3hYko51Y.mp4" raw/nnet.mp4   # neural network 3D simulation
[ -f raw/chip.mp4 ] || cp "$B/U_OexTUIyik.mp4" raw/chip.mp4   # circuit board macro

# "Dark Ambient Drone" by Patrick Lieberkind (FineSound, no copyright): low drone, pulse every 2 s
music woAJrkwRHtU 20

# Hinton only, 11:28.5 to 11:44.85 (Pelley's "Can't afford to get it wrong, why?" follows)
vo hinton 688.5 704.85
words
# whisper got every word right here: words.json is words.raw.json as is
cp words.raw.json words.json

# vertical crop centred on x = $1 (fraction of the 16:9 frame), so faces sit mid-frame
at() { echo "crop=ih*9/16:ih:iw*$1-ih*9/32:0"; }

shot redsrv   redsrv  2.0   1.0 "$DARK"
shot hspot    hinton  670.0 0.9 "$DARK" fill "$(at 0.64)"
shot code     code    20.0  0.8 "$DARK"
shot chip     chip    4.0   0.8 "$DARK"
shot nnet     nnet    60.0  0.8 "$DARK"
shot robot    hinton  203.0 0.8 "$DARK" fill "$(at 0.42)"
shot h100     h100    49.0  0.8 "$DARK"
shot dc       dc      34.0  1.6 "$DARK"
shot hsync    hinton  692.8 2.2 "$DARK" fill "$(at 0.40)"   # in sync with the vo
shot leds     leds    3.0   1.2 "$DARK"
shot young    hinton  109.0 1.9 "$DARK" fill "$(at 0.43)"   # Hinton in the 1970s
shot nnet2    nnet    140.0 1.9 "$DARK"
shot hsync2   hinton  699.1 2.6 "$DARK" fill "$(at 0.40)"   # in sync with the vo
shot redsrv2  redsrv  9.0   1.8 "$DARK"
shot hpost    hinton  713.5 2.0 "$DARK" fill "$(at 0.38)"
shot hhall    hinton  722.0 2.4 "$DARK" fill "$(at 0.57)"
