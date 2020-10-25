#!/bin/env python

# This script is intended to test homeworks written in cpp.

import build_solutions
import os
import sys
import test_homeworks
import validate_input
from validate_input import noexec
import zipfile

validate_input.main()

if zipfile.is_zipfile(sys.argv[1]):
    build_solutions.main()
elif os.path.isdir(sys.argv[1]):
    os.chdir(sys.argv[1])
else:
    print("Usage: ", sys.argv[1], " should be a zipfile containing all the solution or a directory, containing compiled solutions")
    exit(1)

if noexec not in sys.argv:
    test_homeworks.main()
