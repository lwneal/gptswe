import os
import sys
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import gptwc
import io
import pyperclip
import subprocess

PREPROMPT = "Please read all of the following files carefully. Output terse copy-pasteable instructions.\n"
INSTRUCTION = "Instructions: Read the above code. Identify and fix any obvious bugs in a terse but elegant style. Output a brief explanation of each fix.\n"


def get_ignore_spec(repo_path, ignore_paths):
    dotignores = [os.path.join(repo_path, i) for i in ignore_paths]
    ignore_list = [line.strip() for path in dotignores if os.path.exists(path)
                   for line in open(path, 'r')] + [".*", "*.pem", 'venv']
    return PathSpec.from_lines(GitWildMatchPattern, ignore_list)


def process_repository(repo_path, ignore, fp):
    ignore_spec = get_ignore_spec(repo_path, ignore)
    token_count = 0

    # Get a list of all files tracked by git
    tracked_files = subprocess.check_output(["git", "ls-files"], cwd=repo_path, text=True).splitlines()

    for file in tracked_files:
        file_path = os.path.join(repo_path, file)
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


def print_commit_message(args, author_name="GPT-4", author_email="gpt4@openai.com"):
    committer_name = subprocess.check_output(["git", "config", "user.name"]).decode("utf-8").strip()
    committer_email = subprocess.check_output(["git", "config", "user.email"]).decode("utf-8").strip()
    msg = 'Prompt: {}'.format(args.instruction.replace('\n', ' '))
    print(f"\nCOMMITTER_NAME=\"{committer_name}\" COMMITTER_EMAIL=\"{committer_email}\" git commit -a -m \"{msg}\" --author=\"{author_name} <{author_email}>\"\n")


def main():
    par = argparse.ArgumentParser(description="Convert a Git repository into a text format")
    par.add_argument("instruction", nargs="?", default=INSTRUCTION, help="Prompt instructing the model")
    par.add_argument("-o", "--output", default=None, help="Path to the output file")
    par.add_argument("--ignore", nargs='*', default=[".gptignore", ".gitignore"], help="Paths to all ignore files in .gitignore format")
    par.add_argument("--preprompt", default=PREPROMPT, help=f"Text to be displayed before the repository, default {PREPROMPT}")
    par.add_argument("-i", "--inputpath", default=".", help="Path to input Git repository (default $PWD)")
    par.add_argument("--max-tokens", type=int, default=8000, help="Maximum number of tokens to generate")
    par.add_argument("-c", "--clipboard", action="store_true", help="Copy the output to the clipboard")
    par.add_argument("-m", "--commit-message", action="store_true", help="Output a copyable commit message")
    args = par.parse_args()

    fp = io.StringIO()
    fp.write(args.preprompt)
    content_tokens = process_repository(args.inputpath, args.ignore, fp)
    fp.write('Instructions: ' + args.instruction)

    full_output = fp.getvalue()

    if args.commit_message:
        print_commit_message(args)
        return
    elif args.output:
        with open(args.output, 'w') as of:
            of.write(full_output)
    else:
        print(full_output)

    token_count = gptwc.token_count(full_output)
    if token_count > args.max_tokens:
        sys.stderr.write(f"WARNING: {token_count} tokens exceeds the maximum of {args.max_tokens} tokens\nTry adding files to .gptignore or reducing the size of the codebase.\n")

    if args.clipboard:
        full_output = fp.getvalue()
        pyperclip.copy(full_output)
        sys.stderr.write(f"\n{token_count} tokens copied to the clipboard.\n")
    else:
        sys.stderr.write(f"\n{token_count} tokens written to {args.output or 'stdout'}\n")

if __name__ == "__main__":
    main()
