#!/bin/bash

find . -type f -name "*.ui" | sed -e 'p;s/\./_/2' | xargs -n 2 sh -c 'pyuic4 $1 -o $2.py' argv0