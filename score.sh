#!/bin/bash -e

#######################
## !!!!!!!!!!!!!!!!! ##
## !! DO NOT EDIT !! ##
## !!!!!!!!!!!!!!!!! ##
#######################

# This script must NOT be edited. It is used to run your solution against some basic tests.

# Prepare for running solution
echo "Running install.sh first..."
./install.sh
echo "> Done running install.sh"
echo "Running build.sh second..."
./build.sh
echo "> Done running build.sh"

# Run solution
echo "Running tests..."
INPUT_FILE='test-data/01-input.txt'
EXPECTED_OUT=$(cat test-data/01-output.txt)
RUN_OUT=$(./run.sh $INPUT_FILE)
RUN_EXIT=$?
echo "Command: ./run.sh $INPUT_FILE"
echo "Exit Code: $RUN_EXIT"
echo "Output: $RUN_OUT"
echo "Expected: $EXPECTED_OUT"
if [[ "$RUN_OUT" == "$EXPECTED_OUT" ]]; then
    echo "PASSED"
else
    echo "FAILED"
fi
