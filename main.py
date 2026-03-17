import sys

from student import main_student
from teacher import main_teacher

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("using : python script.py [teacher|student]")
        sys.exit(1)

    try:
        funcs = {
            "teacher": main_teacher,
            "student": main_student
        }[sys.argv[1].lower()]()
    except KeyError:
        print("error : arg is 'teacher' or 'student'")
        sys.exit(1)
