#!/bin/env python

import filecmp
import glob
import json
import os
import re
import sys


def create_tasks_list(tests_dir):
    tasks_test_dirs = list()
    for task_test_dir in os.listdir(tests_dir):
        tasks_test_dirs.append(os.path.join(tests_dir, task_test_dir))
    return tasks_test_dirs


def execute_test(test_input, list_student_task_solution):
    expected_test_output = test_input.replace("-in", "-out")
    student_test_output = "/tmp/.tmpfile"
    student_task_solution = re.escape(os.path.join(".", list_student_task_solution))

    command = "echo $(cat " + test_input + " | timeout 1 " + student_task_solution + " | tr [a-z] [A-Z]) > " + student_test_output
    print(command)
    os.system(command)

    test_input_fd = open(test_input)
    expected_test_output_fd = open(expected_test_output)
    student_test_output_fd = open(student_test_output)

    test = dict()
    test["id"] = os.path.basename(test_input)[:-3]
    test["input"] = test_input_fd.read()
    test["expect_output"] = expected_test_output_fd.read()
    test["actual_output"] = student_test_output_fd.read()
    test["match"] = filecmp.cmp(expected_test_output, student_test_output)

    test_input_fd.close()
    expected_test_output_fd.close()
    student_test_output_fd.close()
    os.unlink(student_test_output)

    return test


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return list(atoi(x) for x in re.split(r'(\d+)', text))


def append_student_result(data, student_dir, student_scores, student_tasks):
    data.append({
        "faculty_number": student_dir,
        "score": student_scores,
        "tasks": student_tasks
    })


def dump_results_to_file(data):
    results_file_fd = open(".results.json", "w")
    json.dump(data, results_file_fd)
    results_file_fd.close()


def test_homeworks(students_to_test, tasks_test_dirs):
    data = list()
    for student_dir in students_to_test:
        student_scores = list()
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
                for task_test in sorted(glob.glob(os.path.join(task_test_dir, "*-in")), key=natural_keys):
                    test = execute_test(task_test, list_student_task_solution[0])
                    student_task["tests"].append(test)
                    student_task_score += test["match"]
            student_scores.append(student_task_score)
            student_tasks.append(student_task)
        append_student_result(data, student_dir, student_scores, student_tasks)
        os.chdir("..")
    dump_results_to_file(data)


def main():
    tests_dir = sys.argv[2]
    tasks_test_dirs = create_tasks_list(tests_dir)

    if len(sys.argv) > 3:
        students_to_test = sys.argv[3:]
    else:
        students_to_test = glob.glob("*")
    test_homeworks(students_to_test, tasks_test_dirs)


if __name__ == "__main__":
    main()
