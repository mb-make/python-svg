#!/bin/bash

test="pytest -vv --color=yes"

$test

while [ 1 ]; do
  inotifywait $(find . -maxdepth 4 -type f) -e MODIFY && $test
done
