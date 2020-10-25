#!/bin/env python

import filecmp
import glob
import os
import sys


def create_tasks_list(tests_dir):
    tasks_test_dirs = list()
    for task_test_dir in os.listdir(tests_dir):
        tasks_test_dirs.append(os.path.join(tests_dir, task_test_dir))
    return tasks_test_dirs


def test_homeworks(tests_dir, tasks_test_dirs):
    all_scores_fd = open(".results", "w+")
    for student_dir in glob.glob("*"):
        student_scores = list()
        os.chdir(student_dir)
        for task_test_dir in tasks_test_dirs:
            task_number = os.path.basename(task_test_dir)
            task_score = 0
            for task_test in glob.glob(os.path.join(task_test_dir, "*-in")):
                task_solution = task_test.replace("-in", "-out")
                tmpfile = "tmpfile"
                list_student_file = glob.glob("*_" + task_number + "_*.exe")
                if len(list_student_file) == 0:
                    continue
                student_file = os.path.join(".", list_student_file[0])
                command = "cat " + task_test + " | timeout 2 " + student_file + " > " + tmpfile
                print(command)
                os.system(command)
                if filecmp.cmp(tmpfile, task_solution):
                    task_score += 1
                os.unlink(tmpfile)
            student_scores.append(task_score)
        all_scores_fd.write(student_dir + " " + str(student_scores) + "\n")
        os.chdir("..")
    all_scores_fd.close()


def main(tests_dir):
    tasks_test_dirs = create_tasks_list(tests_dir)
    test_homeworks(tests_dir, tasks_test_dirs)


if __name__ == "__main__":
    tests_dir = sys.argv[1]
    main(tests_dir)
