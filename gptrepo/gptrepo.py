import os
import sys
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

PREPROMPT = "Please read all of the following files. Each file begins with a filename followed by ```` and the sequence of files ends with ``END``\n"
POSTPROMPT = "Instructions: Read the above code. Identify any obvious bugs or security issues and suggest fixes in a terse, elegant, professional style. Tell me the fixes and nothing else.\n"


def get_ignore_spec(repo_path, ignore_paths):
    dotignores = [os.path.join(repo_path, i) for i in ignore_paths]
    ignore_list = [line.strip() for path in dotignores if os.path.exists(path)
                   for line in open(path, 'r')] + [".*", "*.pem"]
    return PathSpec.from_lines(GitWildMatchPattern, ignore_list)


def process_repository(repo_path, ignore, fp):
    ignore_spec = get_ignore_spec(repo_path, ignore)
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relpath = os.path.relpath(file_path, repo_path)
            if not ignore_spec.match_file(relpath):
                with open(file_path, 'r', errors="ignore") as file:
                    contents = file.read()
                fp.write(f"`````\n{relpath}\n````\n{contents}\n")
    fp.write("````\n\n")


def main():
    par = argparse.ArgumentParser(description="Convert a Git repository into a text format")
    par.add_argument("repo_path", nargs="?", default=".", help="Path to the Git repository")
    par.add_argument("-o", "--output", default=None, help="Path to the output file")
    par.add_argument("--ignore", nargs='*', default=[".gptignore", ".gitignore"], help="Paths to the ignore files")
    par.add_argument("--preprompt", default=PREPROMPT, help="Text to be displayed before the repository")
    par.add_argument("--postprompt", default=POSTPROMPT, help="Text to be displayed after the repository")
    args = par.parse_args()

    if args.output is None:
        fp = sys.stdout
    else:
        fp = open(args.output, 'w')

    fp.write(args.preprompt)
    process_repository(args.repo_path, args.ignore, fp)
    fp.write(args.postprompt)

    if args.output:
        print(f"Repository contents written to {args.output}.")

if __name__ == "__main__":
    main()
