#!/bin/bash
# Run fast tests in parallel
pytest -n auto -m "not slow" --test_dir=output

# Run slow tests sequentially
pytest -m "slow" --test_dir=output

# Generate coverage report
coverage report
coverage html