import os, re
from distutils.log import warn as printf

with os.popen('who', 'r') as f:
    for eachLine in f:
        printf(re.split(r'\s\s+|\t', eachLine.strip()))