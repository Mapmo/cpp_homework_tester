#!/usr/bin/env python

from libs import tools_functions
import numpy as np
import sys


def extract_all_scores(results):
    all_scores = list()
    for student in results:
        all_scores.append(student["score"])
    if len(all_scores) <= 0:
        print("Critical error, no scores extracted from", json_file)
        exit(1)
    return all_scores


def calculate_average_tasks(all_results):
    all_results = np.array(all_results)
    all_results_average = list(map(lambda x: round(x, 2), np.average(all_results, axis=0)))
    print("The average score for each task is:", all_results_average)
    return all_results_average


def calculate_average_tasks_tests(tasks):
    average_task_tests = dict()
    for task_id in range(1, tasks + 1):
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
        print("The average score for the tests of each Task #" + str(task_id) + " is: ", average_task_tests[task_id])
    return average_task_tests


argc = len(sys.argv)
if argc < 2 or argc > 5:
    print("Usage:", sys.argv[0], "JSON_FILE [TASK] [TEST_ID]")
    exit(1)

json_file = sys.argv[1]
results = tools_functions.parse_json_file(json_file)
all_scores = extract_all_scores(results)

all_scores_average = calculate_average_tasks(all_scores)
average_task_tests = calculate_average_tasks_tests(len(all_scores_average))

if argc == 2:
    exit(0)

for task_id in range(1, len(all_scores_average) + 1):
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
                    print("Expected output:\n" + test["expect_output"])
                    print("Average score:", average_task_tests[task_id][int(test["id"]) - 1])
                    found_task = True
                break
        if found_task:
            break
