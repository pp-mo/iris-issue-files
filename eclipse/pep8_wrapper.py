"""
A pep8 wrapper for Eclipse.

Only checks the incoming path if it's a '.py' file.

To use with Eclipse:

 - right-click on your project, select properties / builders / new / program

 - in the "main" tab:
   - location = <absolute path of python>
   - arguments = <absolute path of this file> ${build_files:f}

 - in the "build options" tab:
   - check "allocate console"
   - check "during auto-builds" (uncheck everything else)

You'll get pep8 output to the console tab when saving a file.

To do:
Get the output parsed by Eclipse, so we can click on the output.

"""

import pep8
import sys


if __name__ == "__main__":
    print "pep8 wrapper for Eclipse"
    for path in sys.argv[1:]:
        if path.endswith('.py'):
            print path
            print "-" * len(path)
            pep8style = pep8.StyleGuide(quiet=False)
            result = pep8style.input_file(path)
            print result
        else:
            print("ignoring (not a python file) {}".format(path))

