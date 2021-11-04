#!/usr/bin/env python3

import json
import os
from termcolor import colored


def parse_json_file(json_file):
    if not os.path.isfile(json_file):
        print(json_file, "is not a regular file")
        exit(1)
    try:
        with open(json_file) as json_file_fd:
            results = json.load(json_file_fd)
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
    print("No test with id", test_id, "found in the student's tasks. Maybe using '--false' unintentionally?")
    exit(4)

# Used when the HW has 3 tasks and each task earns 3 points
def score_3(score):
    final = None
    if score >= 0.66:
        final = 3.0
    elif score >= 0.33:
        final = 2.0
    elif score > 0:
        final = 1.0
    else:
        final = 0.0
    return final


# Used when the HW has 4 tasks and each task earns 2.5 points
def score_4(score):
    final = None
    if score >= 0.8:
        final = 2.5
    elif score >= 0.6:
        final = 2.0
    elif score >= 0.4:
        final = 1.5
    elif score >= 0.2:
        final = 1.0
    elif score > 0:
        final = 0.5
    else:
        final = 0.0
    return final


# Used when the HW has 5 tasks and each task earns 2 points
def score_5(score):
    final = None
    if score >= 0.8:
        final = 2.0
    elif score >= 0.6:
        final = 1.5
    elif score >= 0.4:
        final = 1.0
    elif score >= 0.2:
        final = 0.5
    else:
        final = 0.0
    return final


def color_score(score, tasks_count):
    final = None
    if tasks_count == 3:
        final = score_3(score)
    elif tasks_count == 4:
        final = score_4(score)
    else:
        final = score_5(score)

    color = None
    if final > 2:
        color = "cyan"
    elif final == 2:
        color = "green"
    elif final >= 1.5:
        color = "yellow"
    elif final >= 1:
        color = "white"
    elif final >= 0.5:
        color = "magenta"
    else:
        color = "red"

    return colored(str(round(score * 100, 2)) + "%\t\t" + str(final) + " points", color)
