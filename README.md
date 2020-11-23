# multi-currency invoice program

This program loads in input data files containing lines of invoice, then outputs
total invoice amount in desired currency.


## How to build/setup

`./docker.sh`. This is the prerequisite step for following operations. In the
following steps, command should be prefixed with CACHE=true, in order to have
a faster feedback loop. Otherwise, `docker build` will take time unnecessarily .


## How to run

`CACHE=true ./docker.sh ./run.sh <path to input json file>`


## How to test

`CACHE=true  ./docker.sh ./test.sh`


## How to update dependencies

- update content in requirement.txt
- rebuild Docker image with `CACHE=false ./docker.sh`


## Assumptions

- line amount should be a positive numeric value
- one valid input JSON file is being used


## Tool of choice

- *nosetests*: It nicely abstracts issues of using relative-path import when running
unittests and the app using run.sh. i.e. When runing test, `import settings`
will cause error "module: setting not found", because tests are not running from
the same Python package(folder), but from root directory.

- *responses*: It mocks the API's response in a quick and determinstic fashion.
