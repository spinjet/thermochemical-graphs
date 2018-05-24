import os
import sys

current_path = sys.path[0]

tree = os.walk(current_path)

for thing in tree:
    print(thing)