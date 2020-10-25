#!/usr/bin/env python

import glob
import shutil
import sys
import time
import os
import zipfile


def unzip_homeworks():
    # Create a new uniq directory where to extract the moodle file that contains all the homeworks
    src_zip = sys.argv[1]
    src_zip = os.path.realpath(sys.argv[1])

    src_zip_name = os.path.split(src_zip)[1]
    os.chdir("/tmp")
    new_dir = src_zip_name + str(time.time())
    os.mkdir(new_dir)
    os.chdir(new_dir)
    with zipfile.ZipFile(src_zip, 'r') as src_zip_obj:
        src_zip_obj.extractall(".")


def create_student_dirs():
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


def remove_moodle_dirs():
    for moodle_dir in glob.glob("[!0-9]*"):
        os.rmdir(moodle_dir)


def compile_homeworks():
    # Compile each file with g++
    for (root, dirs, files) in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".cpp"):
                file_to_compile = os.path.join(root, file)
                file_to_produce = os.path.join(root, file.replace(".cpp", ".exe"))
                command = "g++ '" + file_to_compile + "' -o '" + file_to_produce + "'"
                os.system(command)


def main():
    unzip_homeworks()
    create_student_dirs()
    remove_moodle_dirs()
    compile_homeworks()
