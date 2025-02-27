import os
import sys
import subprocess

# First run test_import.py to verify imports
print("Running test_import.py to verify imports...")
import_result = subprocess.run(
    ["python", "test_import.py"],
    capture_output=True,
    text=True
)

print("IMPORT TEST STDOUT:")
print(import_result.stdout)
print("\nIMPORT TEST STDERR:")
print(import_result.stderr)
print("\nImport test exit code:", import_result.returncode)

# Run the tests with coverage
print("\nRunning pytest with coverage...")
result = subprocess.run(
    [
        "python", "-m", "pytest", "tests/test_basic.py", "-v",
        "--cov=./", "--cov-report=xml", "--cov-config=.coveragerc"
    ],
    capture_output=True,
    text=True
)

# Print the output
print("PYTEST STDOUT:")
print(result.stdout)
print("\nPYTEST STDERR:")
print(result.stderr)
print("\nPytest exit code:", result.returncode)
