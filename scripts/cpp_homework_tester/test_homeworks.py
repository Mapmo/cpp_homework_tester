#!/bin/env python

import filecmp
import glob
import json
import os
import sys


def create_tasks_list(tests_dir):
    tasks_test_dirs = list()
    for task_test_dir in os.listdir(tests_dir):
        tasks_test_dirs.append(os.path.join(tests_dir, task_test_dir))
    return tasks_test_dirs


def execute_test(task_test, list_student_task_solution):
    test_solution = task_test.replace("-in", "-out")
    tmpfile = "tmpfile"
    student_task_solution = os.path.join(".", list_student_task_solution)

    command = "echo $(cat " + task_test + " | timeout 2 " + student_task_solution + " | tr [a-z] [A-Z]) > " + tmpfile
    print(command)
    os.system(command)

    test_solution_fd = open(test_solution)
    tmpfile_fd = open(tmpfile)

    test = dict()
    test["id"] = os.path.basename(task_test)[:-3]
    test["expect_result"] = test_solution_fd.read()
    test["actual_result"] = tmpfile_fd.read()
    test["match"] = filecmp.cmp(test_solution, tmpfile)

    test_solution_fd.close()
    tmpfile_fd.close()
    os.unlink(tmpfile)

    return test


def append_student_result(data, student_dir, student_scores, student_tasks):
    data["results"].append({
        "faculty_number": student_dir,
        "score": student_scores,
        "tasks": student_tasks
    })


def test_homeworks(students_to_test, tasks_test_dirs):
    data = dict()
    data["results"] = list()
    for student_dir in students_to_test:
        student_scores = list()
        student_tasks = list()
        os.chdir(student_dir)
        for task_test_dir in tasks_test_dirs:
            task_number = os.path.basename(task_test_dir)
            list_student_task_solution = glob.glob("*_" + task_number + "_*.exe")
            if len(list_student_task_solution) == 0:
                test = "Compiled solution not found"
                break
            task_score = 0
            student_task = dict()
            student_task["id"] = task_number
            student_task["tests"] = list()
            for task_test in glob.glob(os.path.join(task_test_dir, "*-in")):
                test = execute_test(task_test, list_student_task_solution[0])
                student_task["tests"].append(test)
                if test["match"]:
                    task_score += 1
            student_scores.append(task_score)
            student_tasks.append(student_task)
        append_student_result(data, student_dir, student_scores, student_tasks)
        os.chdir("..")
    results_file = open(".results.json", "w")
    json.dump(data, results_file)


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
