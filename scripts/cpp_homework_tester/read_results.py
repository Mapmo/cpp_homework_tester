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


def extract_student_result(results, faculty_number):
    for student_result in results:
        if student_result["faculty_number"] == faculty_number:
            return student_result
    print("No student with faculty number", faculty_number, "found")
    exit(2)


def extract_student_task(student_result, task_id):
    for student_task in student_result["tasks"]:
        if student_task["id"] == task_id:
            return student_task
    print("No task with id", task_id, "found in the student's results")
    exit(3)


def extract_student_test(student_task, test_id):
    for student_test in student_task["tests"]:
        if student_test["id"] == test_id:
            return student_test
    print("No test with id", test_id, "found in the student's tasks")
    exit(4)


argc = len(sys.argv)
if argc < 2 or argc > 5:
    print("Usage:", sys.argv[0], "JSON_FILE FN TASK_ID TEST_ID")
    exit(1)

json_file = (sys.argv[1])
results = parse_json_file(json_file)
if argc == 2:
    print(json.dumps(results, indent=4))
    exit(0)

faculty_number = sys.argv[2]
student_result = extract_student_result(results, faculty_number)
if argc == 3:
    print(json.dumps(student_result, indent=4))
    exit(0)

task_id = sys.argv[3]
student_task = extract_student_task(student_result, task_id)
if argc == 4:
    print(json.dumps(student_task, indent=4))

test_id = sys.argv[4]
student_test = extract_student_test(student_task, test_id)
print(json.dumps(student_test, indent=4))
