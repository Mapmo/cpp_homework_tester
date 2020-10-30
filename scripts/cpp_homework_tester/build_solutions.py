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


def remove_mac_dir():
    # This function is used for students who use mac and submit __MAC direcotry for some reason
    mac_dirs = glob.glob("*MAC*")
    if len(mac_dirs) > 0:
        for dir in mac_dirs:
            shutil.rmtree(dir)


def remove_useless_dir():
    # This function is for students who zipped a directory containing their homeworks
    if len(glob.glob("*.cpp")) == 0:
        useless_dir = glob.glob("*")[0]
        all_student_files = list()
        for (student_root, student_dirs, student_files) in os.walk(os.getcwd()):
            all_student_files += [os.path.join(student_root, student_file) for student_file in student_files]
        for student_file in all_student_files:
            try:
                shutil.move(student_file, os.getcwd())
            except shutil.Error:
                print("Faculty number", os.path.basename(os.getcwd()), "having no cpp files after unzip")
                shutil.rmtree(os.getcwd())
                return
        os.rmdir(useless_dir)


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
                try:
                    hw_zip_obj.extractall(".")
                except FileExistsError:
                    print("Faculty number", faculty_number, " tried to recreate dir, probably zip in zip submitted. Won't be tested!")
                    os.chdir("..")
                    shutil.rmtree(faculty_number)
                    continue
            os.unlink(homework)
            remove_mac_dir()
            remove_useless_dir()
            os.chdir("..")
        else:
            print("Not a zipfile found while creating the user directories and will be deleted:", homework_path)
            os.unlink(homework_path)


def remove_moodle_dirs():
    for moodle_dir in glob.glob("[!0-9]*"):
        os.rmdir(moodle_dir)


def add_all_libs(original_file):
    # The following function is needed for compiling VS C++ code, since the libraries in VS contain more functions that g++
    original_file_d = open(original_file, encoding='utf-8-sig')  # Using utf-8-sig since some code is written on windows and it may contain characters like <feff>
    original_content = original_file_d.read()
    new_file = original_file + "~"
    new_file_d = open(new_file, "w+")
    new_file_d.write("#include <bits/stdc++.h>\n\n" + original_content.strip())
    original_file_d.close()
    new_file_d.close()
    shutil.move(new_file, original_file)


def compile_homeworks():
    # Compile each file with g++
    for (root, dirs, files) in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".cpp"):
                file_to_compile = os.path.join(root, file)
                add_all_libs(file_to_compile)
                file_to_produce = os.path.join(root, file.replace(".cpp", ".exe"))
                command = "g++ '" + file_to_compile + "' -o '" + file_to_produce + "'"
                print(command)
                os.system(command)


def main():
    unzip_homeworks()
    create_student_dirs()
    remove_moodle_dirs()
    compile_homeworks()
