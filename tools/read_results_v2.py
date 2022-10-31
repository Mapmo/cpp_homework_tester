import argparse
import json

from libs import tools_functions
from termcolor import colored


def remove_successful_tests():
    for task in student_result["tasks"]:
        if isinstance(task["tests"][0], str):
            continue
        for test in range(len(task["tests"]), 0, -1):
            if task["tests"][test - 1]["match"]:
                del task["tests"][test - 1]


parser = argparse.ArgumentParser(description="Read results from results.json generate by cpp_homework_tester-v2")
parser.add_argument("--false", action="store_true", help="Display only failed tests")
parser.add_argument("JSON_FILE", type=str, help="The json file with the results")
parser.add_argument("TASK_ID", type=str, nargs="?")
parser.add_argument("TEST_ID", type=str, nargs="?")
args = parser.parse_args()

json_file = args.JSON_FILE
student_result = tools_functions.parse_json_file(json_file)

if args.false:
    remove_successful_tests()

if not args.TASK_ID:
    print("Student", student_result["student_id"])

    tasks_count = len(student_result["score"])
    if tasks_count == 5:
        grade = tools_functions.grade_5
    elif tasks_count == 4:
        grade = tools_functions.grade_4
    else:
        grade = tools_functions.grade_3

    total = 0
    for task in range(tasks_count):
        task_score = student_result["score"][task]
        points = grade(task_score)
        total += points
        colored_grade = tools_functions.color_score(task_score, points, tasks_count)
        print(f"Task {task + 1}: {colored_grade}")
    print(colored(f"\t\tTotal:\t{total} points", "white"))
    exit(0)


student_task = tools_functions.extract_student_task(student_result, args.TASK_ID)
if not args.TEST_ID:
    print(json.dumps(student_task, indent=4))
    exit(0)

student_test = tools_functions.extract_student_test(student_task, args.TEST_ID)
print(json.dumps(student_test, indent=4))
