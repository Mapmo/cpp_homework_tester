#!/bin/env python3

import sys
import os

notest = "--notest"


def print_usage():
    print("Usage:")
    print("\t" + os.path.basename(sys.argv[0]), "ZIP_FILE TESTS_DIR - will extract all zips from zip_file_all_homeworks, compile the solutions and test them")
    print("\t\t", notest, "- does not run tests, only attempts to compile all files from zip_file_all\n")
    print("\t" + os.path.basename(sys.argv[0]), "HW_DIR TEST_DIR [FN]... - does not compile solutions, HW_DOR is a directory that contains directories named with students ids")
    print("\t\t", "If FNs are passed, the tests will be conducted only for the specified students. The .results file will be overwritten!\n")
    exit(1)


def main():
    argc = len(sys.argv)
    if argc < 3:
        print_usage()

    for arg in sys.argv[1:3]:
        if not os.path.exists(arg):
            print_usage()

    if argc > 3:
        if notest in sys.argv and argc > 4:
            print("Student specified with", notest)
            print_usage()
