#!/bin/env python

import sys
import os
noexec = "--noexec"


def print_usage():
    print("Usage:", os.path.basename(sys.argv[0]), "ZIP_FILE TESTS_DIR - will extract all zips from zip_file_all_homeworks, compile the solutions and test them")
    print("\t\t", noexec, "- does not run tests, only attempts to compile all files from zip_file_all")
    print("\nUsage:", os.path.basename(sys.argv[0]), "HW_DIR TEST_DIR [FN]... - does not compile solutions, HW_DOR is a directory that contains directories named with students ids")
    print("\t\t", "If FNs are passed, the tests will be conducted only for the specified students. The .results file will be overwritten!")
    exit(1)


def main():
    argc = len(sys.argv)
    if argc < 3:
        print_usage()

    for arg in sys.argv[1:2]:
        if not os.path.exists(arg):
            print_usage()

    if argc > 3:
        if noexec in sys.argv and argc > 4:
            print("Student specified with", noexec)
            print_usage()
        for arg in sys.argv[3:]:
            if arg.isnumeric():
                arg_path = os.path.join(sys.argv[1], arg)
                if not os.path.isdir(arg_path):
                    print("No such directory, ", arg_path)
                    print_usage()
            elif arg != noexec:
                print(arg, "is an invalid argument")
                print_usage()
