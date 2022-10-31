import argparse
import glob
import json
import os
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return list(atoi(x) for x in re.split(r"(\d+)", text))


def get_tests_paths(root_tests_dir):
    cwd = os.getcwd()
    os.chdir(root_tests_dir)
    tasks = list()
    for task_dir in glob.glob("*"):
        tasks.append(os.path.join(root_tests_dir, task_dir))
    os.chdir(cwd)
    return sorted(tasks, key=natural_keys)


def execute_test(test_input, list_student_task_solution):
    expected_test_output = test_input.replace("-in", "-out")
    student_test_output = "/tmp/.tmpfile"
    student_task_solution = re.escape(os.path.join(".", list_student_task_solution))

    command = f"cat {test_input} | timeout 1 {student_task_solution} | head -c 500 > {student_test_output}"
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
    with open("results.json", "w") as results_file_fd:
        json.dump(data, results_file_fd)


def test_homeworks(solutions_dir, tests):
    student_score = list()
    student_tasks = list()
    os.chdir(solutions_dir)
    for test_dir in tests:
        task_number = os.path.basename(test_dir)
        # will have issue with double digits tasks, need better file format!
        student_task_solution = glob.glob(f"*{task_number}.exe")
        student_task_score = 0
        student_task = dict()
        student_task["id"] = task_number
        student_task["tests"] = list()
        if len(student_task_solution) == 0:
            test = "Compiled solution not found"
            student_task["tests"].append(test)
        else:
            test_input_files = sorted(
                glob.glob(os.path.join(test_dir, "*-in")), key=natural_keys
            )
            for test_input_file in test_input_files:
                result = execute_test(test_input_file, student_task_solution[0])
                student_task["tests"].append(result)
                student_task_score += result["match"]
            student_task_score = round(student_task_score / len(test_input_files), 2)
        student_score.append(student_task_score)
        student_tasks.append(student_task)
    data = {"student_id": solutions_dir, "score": student_score, "tasks": student_tasks}
    dump_results_to_file(data)


def main():
    parser = argparse.ArgumentParser(description="Test student's homework")
    parser.add_argument("TESTS_DIR", type=str, help="The root directory of the tests")
    parser.add_argument(
        "SOLUTIONS_DIR", type=str, help="The directory with the student's compiled .exe solutions"
    )
    args = parser.parse_args()

    tests = get_tests_paths(args.TESTS_DIR)
    test_homeworks(args.SOLUTIONS_DIR, tests)


if __name__ == "__main__":
    main()
