import argparse
import os
import fnmatch

parser = argparse.ArgumentParser(description='Find files with pattern', add_help=False)
parser.add_argument('--root', nargs=1, required=True)
parser.add_argument('--name', nargs='+')
args = parser.parse_args()

args.name = ['*'] if args.name is None else args.name
matches = []

for root, dirs, files in os.walk(args.root[0]):
        for match in args.name:
            for dir in dirs:
                if fnmatch.fnmatch(dir, match):
                    print(os.path.join(root, dir))
                    matches.append(os.path.join(root, dir))

            for file in files:
                if fnmatch.fnmatch(file, match):
                    print(os.path.join(root, file))
                    matches.append(os.path.join(root, file))


if not matches:
    print("No matches found.")