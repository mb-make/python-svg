#!/bin/bash

while [ 1 ]; do
  inotifywait $(find . -type f -name "*.py") -e MODIFY && pytest -vv --color=yes
done
