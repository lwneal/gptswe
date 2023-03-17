import os
import sys
import fnmatch
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

PRELUDE="The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context.\n"


def get_ignore_spec(repo_path, ignore_paths):
    dotignores = [os.path.join(repo_path, i) for i in ignore_paths]
    ignore_list = [line.strip() for path in dotignores if os.path.exists(path)
                   for line in open(path, 'r')]
    return PathSpec.from_lines(GitWildMatchPattern, ignore_list)


def process_repository(repo_path, ignore_spec, fp):
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relpath = os.path.relpath(file_path, repo_path)
            if not ignore_spec.match_file(relpath):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                fp.write(f"----\n{relpath}\n{contents}\n")


def main():
    par = argparse.ArgumentParser(description="Convert a Git repository into a text format")
    par.add_argument("repo_path", default=".", help="Path to the Git repository")
    par.add_argument("-o", "--output", default=None, help="Path to the output file")
    par.add_argument("--ignore", nargs='*', default=[".gptignore", ".gitignore"], help="Paths to the ignore files")
    args = par.parse_args()


    ignore_spec = get_ignore_spec(args.repo_path, args.ignore)

    with (open(args.output, 'w') if args.output else sys.stdout) as fp:
        process_repository(args.repo_path, ignore_spec, fp)
        fp.write("--END--\n")

    if args.output:
        print(f"Repository contents written to {args.output}.")

if __name__ == "__main__":
    main()
