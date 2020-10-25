#!/bin/env python

# This script is intended to test homeworks written in cpp.

import filecmp
import glob
import os
import sys
import shutil
import time
import zipfile

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "zip_file_all_homeworks tests_directory")
    exit(1)

src_zip = sys.argv[1]
tests_dir = sys.argv[2]
if os.path.exists(src_zip) and zipfile.is_zipfile(src_zip):
    src_zip = os.path.realpath(sys.argv[1])
else:
    print("File", sys.argv[1], " not such zip file found")
    exit(1)

if not os.path.isdir(tests_dir):
    print(tests_dir, " is not a directory")

# Create a new uniq directory where to extract the moodle file that contains all the homeworks
src_zip_name = os.path.split(src_zip)[1]
os.chdir("/tmp")
new_dir = src_zip_name + str(time.time())
os.mkdir(new_dir)
os.chdir(new_dir)
with zipfile.ZipFile(src_zip, 'r') as src_zip_obj:
    src_zip_obj.extractall(".")

# Create a directory for each student based on the faculty number and extract their homework there
all_files = list()
for (root, dirs, files) in os.walk(os.getcwd()):
    all_files += [os.path.join(root, file) for file in files]
for homework_path in all_files:
    homework = os.path.basename(homework_path)
    if zipfile.is_zipfile(homework_path):
        faculty_number = homework.split('_')[2][2:]
        os.mkdir(faculty_number)
        shutil.move(homework_path, faculty_number)
        os.chdir(faculty_number)
        with zipfile.ZipFile(homework, "r") as hw_zip_obj:
            hw_zip_obj.extractall(".")
        os.unlink(homework)
        # This code of block is for students who zipped a directory containing their homeworks
        if len(glob.glob("*.cpp")) == 0:
            useless_dir = glob.glob("*")[0]
            all_student_files = list()
            for (student_root, student_dirs, student_files) in os.walk(os.getcwd()):
                all_student_files += [os.path.join(student_root, student_file) for student_file in student_files]
            for student_file in all_student_files:
                shutil.move(student_file, os.getcwd())
            os.rmdir(useless_dir)
        os.chdir("..")

# Delete the directories generated by moodle for each student, since they are not needed anymore
for useless_dir in glob.glob("[!0-9]*"):
    os.rmdir(useless_dir)

# Compile each file with g++
for (root, dirs, files) in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".cpp"):
            file_to_compile = os.path.join(root, file)
            file_to_produce = os.path.join(root, file.replace(".cpp", ".exe"))
            command = "g++ '" + file_to_compile + "' -o '" + file_to_produce + "'"
            os.system(command)

# Create a list for each task tests
tasks_test_dirs = list()
for task_test_dir in os.listdir(tests_dir):
    tasks_test_dirs.append(os.path.join(tests_dir, task_test_dir))

# Test the student task with a 2 seconds timeout for each test. The final scores are stored in .result file
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
