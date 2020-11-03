#!/usr/bin/env python

from libs import tools_functions
import numpy as np
import sys

argc = len(sys.argv)
if argc > 2:
    print("Usage:", sys.argv[0], "JSON_FILE")
    exit(1)

json_file = (sys.argv[1])
results = tools_functions.parse_json_file(json_file)

all_results = list()
for student in results:
    all_results.append(student["score"])

if len(all_results) <= 0:
    print("Critical error, no results extracted from", json_file)

all_results = np.array(all_results)
all_results_average = list(map(lambda x: round(x, 2), np.average(all_results, axis=0)))
print("The average score for each task is:", all_results_average)
