# Test Suite

This directory contains the test suite for the SonicScribe project.

## Structure

- `integration/`: Contains integration tests for the end-to-end flow of the system.
- `unit/`: Contains unit tests for individual Cloud Functions.
- `data/`: Contains sample test data files used in the tests.

## Running Tests

To run the tests, use the following commands:

- Run integration tests:
  ```bash
  pytest tests/integration/
  ```
- Run unit tests:
  ```bash
  pytest tests/unit/
  ```
