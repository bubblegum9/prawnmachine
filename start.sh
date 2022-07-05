#!/bin/bash
# The tee command reads from the standard input and writes to both standard output and one or more files at the same time.
python3 main.py | tee -a log