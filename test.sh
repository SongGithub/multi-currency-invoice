#!/bin/bash -e

## PLEASE EDIT ME
## Add the commands to test your solution here

docker run --rm \
  -v $PWD:/app -w /app \
  xero-code-test:latest \
  nosetests --verbosity=2
