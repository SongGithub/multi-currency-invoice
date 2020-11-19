# Xero "Multi-Currency Invoice" Code Test

Your objective is to create a simple multi-currency invoicing CLI tool which uses the ExchangeRatesAPI.io historical data API.

## Requirements

__Usage__

Users will execute your program via the `run.sh` helper, and will pass an input filename as the first parameter.

For example, your program should successfully run with the following command:

```
./run.sh test-data/01-input.txt
```

__Input Files__

Your program must read in a JSON file at a path specified relevant to the location of the `run.sh` script.

The input JSON file will contain:

* An invoice date and base currency, along with multiple invoice lines, in JSON format.
* The invoice date will be in the RFC3339 Internet date format e.g. `2020-07-27`
* The invoice base currency will be in ISO4217 alphabetic code format e.g. `NZD`
* Each invoice line should include a description, an decimal amount (to 2 places), and a currency e.g. `AUD`

Example JSON input (per the supplied `test-data/01-input.txt` file):

```
{"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
```

__Actions__

Once your program has successfully read the input file, it should:

* Use the ExchangeRatesAPI.io API to retrieve the exchange rate for each of the currency pairs.
* Calculate each line amount in the base currency, and call it the line total.
* Calculate the invoice total in the base currency.

__Expected Output__

Via stdout only, your program should print:

* On Success: Invoice total in the base currency e.g. `1600.86` followed by a single newline `\n` character
* On Failure: An error message prefixed with `Error: ` followed by a single newline `\n` character

__Assumptions__

* Exchange rates should be calculated at a precision of 4 decimal places - you must round the Exchange Rates API rates before using them to convert line amounts to line totals.
* Line totals and the invoice total only need to be calculated to 2 decimal places - you must round each line total.
* When rounding these numbers, you should round according to standard rules.
  * Rounding should match the [Google Sheets ROUND function](https://support.google.com/docs/answer/3093440?hl=en), for example.

__Example API Call__

A request/response to/from the ExchangeRatesAPI.io API might look like the following:

`GET https://api.exchangeratesapi.io/2020-07-07?base=NZD&symbols=AUD,USD`

```
{"rates":{"USD":0.6541135574,"AUD":0.9421205098},"base":"NZD","date":"2020-07-07"}
```

When converting your line amounts, please pay attention to the direction of the exchange rate you've retrieved from ExchangeRatesAPI.io e.g. USD -> NZD vs NZD -> USD. Each line amount should be converted from the line currency to the invoice currency.

__Programming Language__

Your solution must be implemented in one of the following programming languages:
* C#
* Python
* JavaScript/TypeScript
* Dart
* Go
* Rust
* Java/Kotlin
* PHP
* Swift
* Ruby
* C
* C++

## Provided Material

__Files you must change__

We've provided the following files which we expect you will change:

* `install.sh` should install any dependencies your solution requires to build/test/run.
* `build.sh` should build your solution (if compilation is required).
* `test.sh` should run the tests for your solution.
* `run.sh` should invoke your solution, where any passed parameters get passed on to your implementation via `$@` (see `run.sh` for an example).
* `Dockerfile` except for the first line you should add the tools you need to build/test/run your code to the Dockerfile.
  * Your Dockerfile must be based on the `ubuntu:xenial` image.

__Files you must NOT change__

* `docker.sh` which is a helper for invoking scripts via `docker run`
  * e.g. `./docker.sh install.sh` will run `install.sh` inside an Ubuntu Xenial Docker container.
* `score.sh` which checks that your solution works against some basic test cases.
* `test-data/` directory, with files:
  * `test-data/01-input.txt` - an example JSON input file which `score.sh` will use as input when it tests your program.
  * `test-data/01-ouput.txt` - an example output for the related input file, which `score.sh` will use to assert your program.

## Checking Your Solution

Before you submit your solution to us, we'd like you to check that the following command runs successfully:

`./docker.sh ./score.sh`

_Note: the above command requires Docker to be installed and working on your machine. Alternatively, you could just run `score.sh` locally - but this will be subject to differences in your local environment._

_Note: each time you run `./docker.sh` if an image already exists it will first be removed from the cache via `docker rmi xero-code-test:latest`. To leverage Docker image caching, set `CACHE=true` e.g. `CACHE=true ./docker.sh`_

## Submission Format

Please ZIP your project folder, including a `.git` directory with at least one commit, and provide this to our recruiter.

## Evaluation Criteria

1. We will check that you have correctly followed the instructions per this document.

2. After reviewing your code, we will attempt to run your solution against the provided `score.sh` script inside a Docker container.

3. We will run your code against a more extensive version of that `score.sh` script, with addition `test-data/` files, to evaluate additional edge cases.

4. We will score your submission against:

   * Code Design
   * Quality
   * Error Handling
   * Code Performance
   * Security
   * Operability
   * Documentation

## Time Limits

We expect a solution can be completed within 1-3 hours total development time.

Please do not attempt to add additional features we have not asked for. We want a working solution which addresses our evaluation criteria - nothing more.

If you do not believe you can complete a solution in under 3 hours, please let us know. We do not "police" this time limit - it simply exists to be respectful of your time.
