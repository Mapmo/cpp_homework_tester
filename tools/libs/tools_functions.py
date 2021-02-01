#!/usr/bin/env python

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


# Used when the HW has 5 tasks and each task earns 2 points
def color_score_3(score):
    color = None
    final = None
    if score >= 0.66:
        color = "green"
        final = "3"
    elif score >= 0.33:
        color = "yellow"
        final = "2"
    elif score > 0:
        color = "white"
        final = "1"
    else:
        color = "red"
        final = "0"
    return colored(str(round(score * 100, 2)) + "%\t\t" + final + " points", color)


# Used when the HW has 5 tasks and each task earns 2 points
def color_score_5(score):
    color = None
    final = None
    if score >= 0.8:
        color = "green"
        final = "2"
    elif score >= 0.6:
        color = "yellow"
        final = "1.5"
    elif score >= 0.4:
        color = "white"
        final = "1"
    elif score >= 0.2:
        color = "magenta"
        final = "0.5"
    else:
        color = "red"
        final = "0"
    return colored(str(round(score * 100, 2)) + "%\t\t" + final + " points", color)


# Used when the HW has 4 tasks and each task earns 2.5 points
def color_score_4(score):
    color = None
    final = None
    if score >= 0.8:
        color = "green"
        final = "2.5"
    elif score >= 0.6:
        color = "yellow"
        final = "2"
    elif score >= 0.4:
        color = "blue"
        final = "1.5"
    elif score >= 0.2:
        color = "white"
        final = "1"
    elif score > 0:
        color = "magenta"
        final = "0.5"
    else:
        color = "red"
        final = "0"
    return colored(str(round(score * 100, 2)) + "%\t\t" + final + " points", color)
