#!/bin/bash

# Steps to test cellom2tif:
# 1. edit the alias declaration below to point to the right Fiji binary
# 2. Run this script from the cellom2tif directory

fiji="/Applications/Fiji.app/Contents/MacOS/fiji-macosx --headless"
# common Fiji binary locations
# OSX: /Applications/Fiji.app/Contents/MacOS/fiji-macosx
# Linux: ~/Downloads/Fiji.app/ImageJ-linux64

$fiji cellom2tif.py test-data test-data-out
if [ `diff -r test-data-out test-data-results | wc -l` -eq 0 ]; then
    echo "full conversion passed"
    rm -rf test-data-out
else
    echo "full conversion failed"
    echo "use verify.py on 'test-data-out' and 'test-data-results'"
    diff -r test-data-out test-data-results
fi

$fiji cellom2tif.py -m test-data test-data-out-m
if [ `diff -r test-data-out-m test-data-results-m | wc -l` -eq 0 ]; then
    echo "ignore mask conversion passed"
    rm -rf test-data-out-m
else
    echo "ignore mask conversion failed"
    echo "use verify.py on 'test-data-out-m' and 'test-data-results-m'"
    diff -r test-data-out-m test-data-results-m
fi

