#!/usr/bin/env python

import glob
import os
import re
import shutil
import sys
import zipfile


def unzip_homeworks():
    # Create a new uniq directory where to extract the moodle file that contains all the homeworks
    src_zip = sys.argv[1]
    src_zip = os.path.realpath(sys.argv[1])

    src_zip_name = os.path.split(src_zip)[1]
    os.chdir("/tmp")
    new_dir = src_zip_name[:-4]
    os.mkdir(new_dir)
    os.chdir(new_dir)
    with zipfile.ZipFile(src_zip, 'r') as src_zip_obj:
        src_zip_obj.extractall(".")


def extract_faculty_number(homework_path, homework):
    try:
        faculty_number = re.findall("(\d(?:MI)?\d+)", homework.split('_')[2])[0]
        return faculty_number
    except IndexError:
        print("Failed to extract faculty number from", homework_path)
    os.unlink(homework_path)
    return -1


def remove_mac_dir():
    # This function is used for students who use mac and submit __MAC direcotry for some reason
    mac_dirs = glob.glob("*MAC*")
    if len(mac_dirs) > 0:
        for dir in mac_dirs:
            shutil.rmtree(dir)


def move_student_homework(student_homework):
    try:
        shutil.move(student_homework, os.getcwd())
    except shutil.Error:
        print("Faculty number", os.path.basename(os.getcwd()), "having no cpp files after unzip")
        shutil.rmtree(os.getcwd())
        return -1


def remove_zipped_dir(faculty_number):
    # This function is for students who zipped a directory containing their homeworks
    if len(glob.glob("*.cpp")) == 0:
        zipped_dir = glob.glob("*")[0]
        all_student_homeworks = list()
        for (student_root, student_dirs, student_homeworks) in os.walk(os.getcwd()):
            all_student_homeworks += [os.path.join(student_root, student_homework) for student_homework in student_homeworks]
        for student_homework in all_student_homeworks:
            if move_student_homework(student_homework) == -1:
                return
        try:
            os.rmdir(zipped_dir)
        except OSError:
            print("Zipped directory of", faculty_number, "not empty")
            shutil.rmtree(zipped_dir)


def create_student_dirs():
    # Create a directory for each student based on the faculty number and extract their homework there
    all_files = list()
    for (root, dirs, files) in os.walk(os.getcwd()):
        all_files += [os.path.join(root, file) for file in files]
    for homework_path in all_files:
        homework = os.path.basename(homework_path)
        if zipfile.is_zipfile(homework_path):
            faculty_number = extract_faculty_number(homework_path, homework)
            if faculty_number == -1:
                continue
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
            remove_zipped_dir(faculty_number)
            os.chdir("..")
        else:
            print("File", os.path.basename(homework_path), "is not a zip file and student wont have his homework tested")
            os.unlink(homework_path)


def remove_moodle_dirs():
    for moodle_dir in glob.glob("*[!0-9]*"):
        os.rmdir(moodle_dir)


def check_for_system_calls(file_to_compile):
    try:
        with open(file_to_compile, encoding="utf-8-sig") as file_to_compile_fd:  # Using utf-8-sig since some code is written on windows and it may contain characters like <feff>
            for line in file_to_compile_fd:
                if re.search("system\(", line):
                    return 2
    except UnicodeDecodeError:
        return 1
    return 0


def add_all_libs(original_file):
    # The following function is needed for compiling VS C++ code, since the libraries in VS contain more functions that g++
    with open(original_file, encoding="utf-8-sig") as original_file_d:  # Using utf-8-sig since some code is written on windows and it may contain characters like <feff>
        original_content = original_file_d.read()
        new_file = original_file + "~"
        with open(new_file, "w+") as new_file_d:
            libs_to_add = ["cmath", "climits", "limits"]
            for lib in libs_to_add:
                new_file_d.write("#include <" + lib + ">\n")
            new_file_d.write(original_content.strip())
    shutil.move(new_file, original_file)


def compile_homeworks():
    # Compile each file with g++
    for (root, dirs, files) in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".cpp"):
                file_to_compile = os.path.join(root, file)
                invalid = check_for_system_calls(file_to_compile)
                if invalid > 0:
                    if invalid == 1:
                        print("File", os.path.basename(file_to_compile), "cannot be opened for reading in utf-8-signed and won't be compiled")
                    else:
                        print("File", os.path.basename(file_to_compile), "contails system() calls and won't be compiled")
                    continue
                add_all_libs(file_to_compile)
                file_to_produce = os.path.join(root, file.replace(".cpp", ".exe"))
                command = "g++ '" + file_to_compile + "' -o '" + file_to_produce + "' 2> /dev/null || exit 1"

                if os.system(command) != 0:
                    print("File", os.path.basename(file_to_compile), "failed to compile")


def main():
    unzip_homeworks()
    create_student_dirs()
    remove_moodle_dirs()
    compile_homeworks()
