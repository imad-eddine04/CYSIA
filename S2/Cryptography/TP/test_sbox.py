#!/usr/bin/env python
# Test script for S-Box with automated inputs

import subprocess
import sys

# Run the S-Box script with automated inputs
# Input sequence: empty (use default 'A'), empty (use default 'Hello World'), 'Hello CBC'
process = subprocess.Popen(
    [sys.executable, 'S-Box.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Provide inputs: press Enter 3 times (use all defaults)
inputs = "\n\n\n"
stdout, stderr = process.communicate(input=inputs)

print(stdout)
if stderr:
    print("STDERR:", stderr)
