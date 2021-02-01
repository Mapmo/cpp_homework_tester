#!/bin/env python

import glob
import json
import os
import re
import sys

execute_dir = ''


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return list(atoi(x) for x in re.split(r'(\d+)', text))


def create_tasks_list(tests_dir):
    cwd = os.getcwd()
    os.chdir(tests_dir)  # used when the zip file for build_solutions is in a separate directory and user uses relative paths
    tasks_test_dirs = list()
    for task_test_dir in glob.glob('*'):
        tasks_test_dirs.append(os.path.join(tests_dir, task_test_dir))
    os.chdir(cwd)
    return sorted(tasks_test_dirs, key=natural_keys)


def execute_test(test_input, list_student_task_solution):
    expected_test_output = test_input.replace("-in", "-out")
    student_test_output = "/tmp/.tmpfile"
    student_task_solution = re.escape(os.path.join(".", list_student_task_solution))

    command = "echo $(cat " + test_input + " | timeout 1 " + student_task_solution + " | tr [a-z] [A-Z] | head -c 100) > " + student_test_output
    os.system(command)

    with open(test_input) as test_input_fd:
        with open(expected_test_output) as expected_test_output_fd:
            with open(student_test_output) as student_test_output_fd:
                test = dict()
                test["id"] = os.path.basename(test_input)[:-3]
                test["input"] = test_input_fd.read()
                test["expect_output"] = expected_test_output_fd.read().strip()
                try:
                    test["actual_output"] = student_test_output_fd.read().strip()
                except UnicodeDecodeError:
                    print("File", student_task_solution, "produces some unicode issues")
                    test["actual_output"] = "encoding issue"
                test["match"] = test["expect_output"] == test["actual_output"]

    os.unlink(student_test_output)
    return test


def append_student_result(data, student_dir, student_scores, student_tasks):
    data.append({
        "faculty_number": student_dir,
        "score": student_scores,
        "tasks": student_tasks
    })


def dump_results_to_file(data):
    with open(".results.json", "w") as results_file_fd:
        json.dump(data, results_file_fd)


def test_homeworks(students_to_test, tasks_test_dirs):
    data = list()
    for student_dir in students_to_test:
        student_score = list()
        student_tasks = list()
        os.chdir(student_dir)
        for task_test_dir in tasks_test_dirs:
            task_number = os.path.basename(task_test_dir)
            list_student_task_solution = glob.glob("*_" + task_number + "_*.exe")
            student_task_score = 0
            student_task = dict()
            student_task["id"] = task_number
            student_task["tests"] = list()
            if len(list_student_task_solution) == 0:
                test = "Compiled solution not found"
                student_task["tests"].append(test)
            else:
                task_tests = sorted(glob.glob(os.path.join(task_test_dir, "*-in")), key=natural_keys)
                for task_test in task_tests:
                    test = execute_test(task_test, list_student_task_solution[0])
                    student_task["tests"].append(test)
                    student_task_score += test["match"]
                student_task_score = round(student_task_score / len(task_tests), 2)
            student_score.append(student_task_score)
            student_tasks.append(student_task)
        append_student_result(data, student_dir, student_score, student_tasks)
        os.chdir("..")
    dump_results_to_file(data)


def main():
    tests_dir = os.path.join(execute_dir, sys.argv[2])
    tasks_test_dirs = create_tasks_list(tests_dir)
    if len(sys.argv) > 3:
        students_to_test = sys.argv[3:]
    else:
        students_to_test = sorted(glob.glob("*"))
    test_homeworks(students_to_test, tasks_test_dirs)


if __name__ == "__main__":
    main()
