#!/usr/bin/env python3

import json
import sys

from libs import tools_functions
from termcolor import colored

false_option = "--false"


def check_for_false_option():
    if false_option in sys.argv:
        sys.argv.remove(false_option)
        return True
    return False


def remove_successful_tests():
    for student in results:
        for task in student["tasks"]:
            if isinstance(task["tests"][0], str):
                continue
            for test in range(len(task["tests"]), 0, -1):
                if task["tests"][test - 1]["match"]:
                    del task["tests"][test - 1]


false_option_set = check_for_false_option()
argc = len(sys.argv)
if argc < 2 or argc > 5:
    print("Usage:")
    print("\t" + sys.argv[0], "JSON_FILE [[[FN] [TASK_ID] [TEST_ID]]]")
    print("\t\t" + false_option, "- prints only the tests that appear to have failed the testing\n")
    exit(1)


json_file = (sys.argv[1])
results = tools_functions.parse_json_file(json_file)

if false_option_set:
    remove_successful_tests()

if argc == 2:
    print(json.dumps(results, indent=4))
    exit(0)

faculty_number = sys.argv[2]
student_result = tools_functions.extract_student_result(results, faculty_number)
if argc == 3:
    print("Student", student_result["faculty_number"])

    tasks_count = len(student_result["score"])
    if tasks_count == 5:
        score = tools_functions.score_5
    elif tasks_count == 4:
        score = tools_functions.score_4
    else:
        score = tools_functions.score_3

    total = 0
    for task in range(tasks_count):
        task_score = student_result["score"][task]
        points = score(student_result["score"][task])
        total += points
        colored_score = tools_functions.color_score(task_score, tasks_count)
        print("Task", task + 1, ":", colored_score)
    print(colored("\t\t\t" + str(total) + " points", 'white'))
    exit(0)

task_id = sys.argv[3]
student_task = tools_functions.extract_student_task(student_result, task_id)
if argc == 4:
    print(json.dumps(student_task, indent=4))
    exit(0)

test_id = sys.argv[4]
student_test = tools_functions.extract_student_test(student_task, test_id)
print(json.dumps(student_test, indent=4))
