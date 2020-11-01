#!/usr/bin/env python

import json
import sys
import os


def parse_json_file(json_file):
    if not os.path.isfile(json_file):
        print(json_file, "is not a regular file")
        exit(1)
    json_file_fd = open(json_file)
    json_file_data = json_file_fd.read()
    json_file_fd.close()
    try:
        results = json.loads(json_file_data)
    except ValueError:
        print(json_file, "not a valid json file")
        exit(1)
    return results


argc = len(sys.argv)
if argc < 2 or argc > 4:
    print("Usage:", sys.argv[0], "JSON_FILE FN TASK_ID TEST_ID")
    exit(1)

json_file = (sys.argv[1])
results = parse_json_file(json_file)

if argc == 2:
    print(json.dumps(results, indent=4))
    exit(0)

json_file_dir = os.path.dirname(json_file)
faculty_number = sys.argv[2]

student_matched = False
for student in results:
    if student["faculty_number"] == faculty_number:
        student_result = student
        student_matched = True
        break

if not student_matched:
    print("No student with faculty number", faculty_number, "found")
    exit(2)

if argc == 3:
    print(json.dumps(student, indent=4))
