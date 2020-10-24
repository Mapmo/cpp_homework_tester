#!/bin/env python

# This script is intended to test homeworks written in cpp.

import os
import sys
import time
import zipfile

if len(sys.argv) != 2:
    print("Pass the location of the zipfile, containing all the homeworks")
    exit(1)

src_zip = sys.argv[1]
if os.path.exists(src_zip) and zipfile.is_zipfile(src_zip):
    src_zip = os.path.realpath(sys.argv[1])
else:
    print("File", sys.argv[1], " not such zip file found")
    exit(1)

# Create a uniq directory for zip extraction
src_zip_name = os.path.split(src_zip)[1]
os.chdir("/tmp")
new_dir = src_zip_name + str(time.time())
os.mkdir(new_dir)
os.chdir(new_dir)


with zipfile.ZipFile(src_zip, 'r') as src_zip_obj:
    src_zip_obj.extractall(".")
