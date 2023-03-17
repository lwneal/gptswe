import os
import sys
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import gptwc

PREPROMPT = "Please read all of the following files. Each file begins with a filename followed by ```` and the sequence of files ends with ``END``\n"
INSTRUCTION = "Instructions: Read the above code. Identify any obvious bugs or security issues and suggest fixes in a terse, elegant, professional style. Show me each fixed line of code, with comments explaining each fix.\n"


def get_ignore_spec(repo_path, ignore_paths):
    dotignores = [os.path.join(repo_path, i) for i in ignore_paths]
    ignore_list = [line.strip() for path in dotignores if os.path.exists(path)
                   for line in open(path, 'r')] + [".*", "*.pem"]
    return PathSpec.from_lines(GitWildMatchPattern, ignore_list)


def process_repository(repo_path, ignore, fp):
    ignore_spec = get_ignore_spec(repo_path, ignore)
    token_count = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relpath = os.path.relpath(file_path, repo_path)
            if not ignore_spec.match_file(relpath):
                with open(file_path, 'r', errors="replace") as file:
                    contents = file.read()
                text = f"`````\n{relpath}\n````\n{contents}\n"
                token_count += gptwc.token_count(text)
                fp.write(text)
    text = "````\n\n"
    token_count += gptwc.token_count(text)
    fp.write(text)
    return token_count


def main():
    par = argparse.ArgumentParser(description="Convert a Git repository into a text format")
    par.add_argument("repo_path", nargs="?", default=".", help="Path to the Git repository")
    par.add_argument("-o", "--output", default=None, help="Path to the output file")
    par.add_argument("--ignore", nargs='*', default=[".gptignore", ".gitignore"], help="Paths to the ignore files")
    par.add_argument("--preprompt", default=PREPROMPT, help="Text to be displayed before the repository")
    par.add_argument("-i", "--instruction", default=INSTRUCTION, help="Instruction text displayed at the end")
    args = par.parse_args()

    if args.output is None:
        fp = sys.stdout
    else:
        fp = open(args.output, 'w')

    fp.write(args.preprompt)
    content_tokens = process_repository(args.repo_path, args.ignore, fp)
    fp.write(args.instruction)

    token_count = gptwc.token_count(args.preprompt) + content_tokens + gptwc.token_count(args.instruction)
    sys.stderr.write(f"\n{token_count} tokens written to {args.output or 'stdout'}\n")

if __name__ == "__main__":
    main()
