#!/usr/bin/env bash
python3 -c "import math; ys = [[math.sin(i/(10+i/50)) - math.sin(i/100) for i in range(1000)], [math.sin(i/(10+i/50)) - math.sin(i/100) - 1 for i in range(900)]]; from uniplot import plot; plot(ys, lines=True, x_unit='s', title='Double sine wave', interactive=True)"
