import os
import sys
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import gptwc

PREPROMPT = "Please read all of the following files carefully.\n"
INSTRUCTION = "Instructions: Read the above code. Identify and fix any obvious bugs in a terse but elegant style. Output a brief explanation of each fix.\n"


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
                with open(file_path, 'r') as file:
                    try:
                        contents = file.read()
                    except UnicodeDecodeError:
                        continue
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
    par.add_argument("--max-tokens", type=int, default=8000, help="Maximum number of tokens to generate")
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
    if token_count > args.max_tokens:
        sys.stderr.write(f"WARNING: {token_count} tokens exceeds the maximum of {args.max_tokens} tokens\nTry adding files to .gptignore or reducing the size of the codebase.\n")

if __name__ == "__main__":
    main()
