#!/bin/env python

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
    print("Error: '" + sys.argv[1] + "' not a zipfile or directory")
    validate_input.print_usage()
    exit(1)

if noexec not in sys.argv:
    test_homeworks.main()
