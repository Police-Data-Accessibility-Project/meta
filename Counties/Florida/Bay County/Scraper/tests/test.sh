#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

trap 'kill $(jobs -p) >&/dev/null' EXIT

if [[ -z "$DISPLAY" ]]; then
    # If you're on a headless server, spin up a virtual framebuffer
    # (or use display :99 if it exists).
    [[ -e /tmp/.X99-lock ]] || Xvfb :99 &
fi

DISPLAY=:99 PYTHONPATH="$DIR/.." pytest
