#!/usr/bin/env python

from libs import tools_functions
import numpy as np
import sys

argc = len(sys.argv)
if argc > 2:
    print("Usage:", sys.argv[0], "JSON_FILE")
    exit(1)

json_file = (sys.argv[1])
results = tools_functions.parse_json_file(json_file)

all_results = list()
for student in results:
    all_results.append(student["score"])

if len(all_results) <= 0:
    print("Critical error, no results extracted from", json_file)

all_results = np.array(all_results)
all_results_average = list(map(lambda x: round(x, 2), np.average(all_results, axis=0)))
print("The average score for each task is:", all_results_average)

average_task_tests = dict()
for task_id in range(1, len(all_results_average) + 1):
    current_task_tests = list()
    for student in results:
        for task in student["tasks"]:
            if task["id"] == str(task_id):
                student_task_tests = list()
                for test in task["tests"]:
                    try:
                        student_task_tests.append(int(test["match"]))
                    except TypeError:
                        break
                if len(student_task_tests) > 0:
                    current_task_tests.append(student_task_tests)
                break
    current_task_tests = np.array(current_task_tests)
    average_current_task_tests = list(map(lambda x: round(x, 2), np.average(current_task_tests, axis=0)))
    average_task_tests[task_id] = average_current_task_tests

for task_id in average_task_tests.keys():
    print("The average result for the tests of each Task #" + str(task_id) + " is: ", average_task_tests[task_id])
for task_id in range(1, len(all_results_average) + 1):
    found_task = False
    for student in results:
        for task in student["tasks"]:
            if task["id"] == str(task_id):
                if type(task["tests"][0]) is not dict:
                    continue
                for test in task["tests"]:
                    print("------------------------------------------")
                    print("Test", task["id"] + "-" + test["id"])
                    print("\nInput:\n" + test["input"])
                    print("Expected output\n" + test["expect_output"])
                    print("Average score:", average_task_tests[task_id][int(test["id"]) - 1])
                    found_task = True
                break
        if found_task:
            break
