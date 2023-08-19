#!/bin/bash

CONF_DIR="confs/*"

for _f in $CONF_DIR; do
    ## Skip cmdline.txt
    [[ $_f == *.txt ]] && continue
    cloud-init schema --config-file $_f
done
