#!/usr/bin/env python3

import json
import os
from termcolor import colored


def parse_json_file(json_file):
    if not os.path.isfile(json_file):
        print(f"{json_file} is not a regular file")
        exit(1)
    try:
        with open(json_file) as json_file_fd:
            results = json.load(json_file_fd)
    except ValueError:
        print(f"{json_file} not a valid json file")
        exit(1)
    return results


def extract_student_result(results, faculty_number):
    for student_result in results:
        if student_result["faculty_number"] == faculty_number:
            return student_result
    print(f"No student with faculty number {faculty_number} found")
    exit(2)


def extract_student_task(student_result, task_id):
    for student_task in student_result["tasks"]:
        if student_task["id"] == task_id:
            return student_task
    print(f"No task with id {task_id} found in the student's results")
    exit(3)


def extract_student_test(student_task, test_id):
    for student_test in student_task["tests"]:
        if student_test["id"] == test_id:
            return student_test
    print(
        f"No test with id {test_id} found in the student's tasks. Maybe using '--false' unintentionally?"
    )
    exit(4)


# Used when the HW has 3 tasks and each task earns 3 points
def grade_3(score):
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
def grade_4(score):
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
def grade_5(score):
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


def pick_color(final):
    if final > 2:
        return "cyan"
    elif final == 2:
        return "green"
    elif final >= 1.5:
        return "yellow"
    elif final >= 1:
        return "white"
    elif final >= 0.5:
        return "magenta"
    else:
        return "red"


def color_score(score, final, tasks_count):
    color = pick_color(final)
    return colored(str(round(score * 100, 2)) + "%\t\t" + str(final) + " points", color)
