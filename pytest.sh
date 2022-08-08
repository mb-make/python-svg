#!/bin/bash

test="pytest -vv --color=yes"

$test

while [ 1 ]; do
  $test -r . 2>&1
  sleep 3
  inotifywait $(find . -maxdepth 4 -type f) -e MODIFY 2>&1
done
