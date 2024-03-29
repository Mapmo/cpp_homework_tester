import glob
import json
import os
import re
import sys

execute_dir = ""


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return list(atoi(x) for x in re.split(r"(\d+)", text))


def create_tasks_list(tests_dir):
    cwd = os.getcwd()
    os.chdir(
        tests_dir
    )  # used when the zip file for build_solutions is in a separate directory and user uses relative paths
    tasks = list()
    for task_dir in glob.glob("*"):
        tasks.append(os.path.join(tests_dir, task_dir))
    os.chdir(cwd)
    return sorted(tasks, key=natural_keys)


def execute_test(test_input, list_student_task_solution):
    expected_test_output = test_input.replace("-in", "-out")
    student_test_output = "/tmp/.tmpfile"
    student_task_solution = re.escape(os.path.join(".", list_student_task_solution))

    command = f"cat {test_input} | timeout 1 {student_task_solution} | head -c 300 > {student_test_output}"
    os.system(command)

    with open(test_input) as test_input_fd:
        with open(expected_test_output) as expected_test_output_fd:
            with open(student_test_output) as student_test_output_fd:
                test = dict()
                test["id"] = os.path.basename(test_input)[:-3]
                test["input"] = test_input_fd.read()
                test["expect_output"] = expected_test_output_fd.read().strip().lower()
                try:
                    test["actual_output"] = (
                        student_test_output_fd.read().strip().lower()
                    )
                except UnicodeDecodeError:
                    print(f"File {student_task_solution} produces some unicode issues")
                    test["actual_output"] = "encoding issue"
                test["match"] = test["expect_output"] == test["actual_output"]

    os.unlink(student_test_output)
    return test


def append_student_result(data, student_dir, student_scores, student_tasks):
    data.append(
        {"faculty_number": student_dir, "score": student_scores, "tasks": student_tasks}
    )


def dump_results_to_file(data):
    with open(".results.json", "w") as results_file_fd:
        json.dump(data, results_file_fd)


def test_homeworks(students_to_test, tasks):
    data = list()
    for student_dir in students_to_test:
        student_score = list()
        student_tasks = list()
        os.chdir(student_dir)
        for task_id in tasks:
            task_number = os.path.basename(task_id)
            student_task_solution = glob.glob(f"*_{task_number}_*.exe")
            student_task_score = 0
            student_task = dict()
            student_task["id"] = task_number
            student_task["tests"] = list()
            if len(student_task_solution) == 0:
                test = "Compiled solution not found"
                student_task["tests"].append(test)
            else:
                task_tests = sorted(
                    glob.glob(os.path.join(task_id, "*-in")), key=natural_keys
                )
                for test in task_tests:
                    test_result = execute_test(test, student_task_solution[0])
                    student_task["tests"].append(test_result)
                    student_task_score += test_result["match"]
                student_task_score = round(student_task_score / len(task_tests), 2)
            student_score.append(student_task_score)
            student_tasks.append(student_task)
        append_student_result(data, student_dir, student_score, student_tasks)
        os.chdir("..")
    dump_results_to_file(data)


def main():
    tests_dir = os.path.join(execute_dir, sys.argv[2])
    tasks = create_tasks_list(tests_dir)
    if len(sys.argv) > 3:
        students_to_test = sys.argv[3:]
    else:
        students_to_test = sorted(glob.glob("*"))
    test_homeworks(students_to_test, tasks)


if __name__ == "__main__":
    main()
