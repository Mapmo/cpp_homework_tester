This script is intended to test homeworks written in cpp.

The main file is cpp_homework_tester.py and depending on the parameters passed, it calls the other files

To get information about the script, just execute it and a usage text will be printed

All tests that contain letters should contain only uppercase letters, since it is hard for students to follow exact patterns.

How to use the scripts in the project:
<ul>
	<li>
		cpp_homework_tester.py:
		<ul>
			<li>
				cpp_homework_tester.py ZIP_FILE TESTS_DIR - will extract all zips from zip_file_all_homeworks, compile the solutions and test them </br>
				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--notest - does not run tests, only attempts to compile all files from zip_file_all
			</li>
			<li>
				cpp_homework_tester.py HW_DIR TEST_DIR [FN]... - does not compile solutions, HW_DIR is a directory that contains directories named with students ids </br>
			<li>
				 If FNs are passed, the tests will be conducted only for the specified students. The .results file will be overwritten!
			</li>
		</ul>
	</li>
	<li>
		How to use tools/read_results.py
		<ul>
			<li> Usage: tools/read_results.py JSON_FILE [[[FN] [TASK_ID] [TEST_ID]]] </br>
			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--false - prints only the tests that appear to have failed the testing </li>
		</ul>
	</li>
	<li>
		How to use tools/read_results.py
		<ul>
			<li> Usage: tools/analyze_results.py JSON_FILE [TASK] [TEST_ID] </li>
		</ul>
	</li>
</ul>
