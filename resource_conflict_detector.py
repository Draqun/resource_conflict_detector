import argparse
import code_parser
import fnmatch as fm
import mimetypes
import os
from rcd import cpp_files_mimetype
import sys


def main(dir):
    if not os.path.isdir(dir):
        print("dir argument is not a path to directory!", file=sys.stderr)
        return 1

    functions, threads, timeframes = [], [], []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        type = mimetypes.guess_type(file)
        if not fm.fnmatch(file_path, "*.cpp") or type[0] != cpp_files_mimetype:
            continue

        with open(file_path, "rt") as f:
            tmp_functions, tmp_threads = [], []
            code_parser.parse_code(f.read(), tmp_functions, tmp_threads, timeframes)
        functions.extend(tmp_functions)
        threads.extend(tmp_threads)

    for t in threads:
        t.can_generate_deadlock()


if "__main__" == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Path to directory with C app")
    args = parser.parse_args()
    main(args.dir)
