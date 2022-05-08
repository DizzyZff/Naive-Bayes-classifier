from learn import *
from test import *
import sys


def main():
    input_file = sys.argv[1]
    N = int(sys.argv[2])

    X = Test(input_file, N)
    # compose output file
    print(X.output_string)
    output_file = open("Output.txt", "w")
    output_file.write(X.output_string)


if __name__ == '__main__':
    main()
    sys.exit(0)