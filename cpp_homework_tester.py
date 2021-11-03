#!/bin/env python3

import os
import sys
import zipfile

from libs import build_solutions
from libs import test_homeworks
from libs import validate_input

from libs.validate_input import notest

validate_input.main()
test_homeworks.execute_dir = os.getcwd()

if zipfile.is_zipfile(sys.argv[1]):
    build_solutions.main()
elif os.path.isdir(sys.argv[1]):
    os.chdir(sys.argv[1])
else:
    print("Error: '" + sys.argv[1] + "' not a zipfile or directory")
    validate_input.print_usage()
    exit(1)

if notest in sys.argv:
	exit(0)

test_homeworks.main()
