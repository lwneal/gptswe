import os
import sys
import fnmatch
import argparse

def get_ignore_list(ignore_file_path):
    ignore_list = []
    with open(ignore_file_path, 'r') as ignore_file:
        for line in ignore_file:
            ignore_list.append(line.strip())
    return ignore_list

def should_ignore(file_path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_repository(repo_path, ignore_list, output_file):
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                output_file.write("-" * 4 + "\n")
                output_file.write(f"{relative_file_path}\n")
                output_file.write(f"{contents}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert a Git repository into a text format")
    parser.add_argument("repo_path", help="Path to the Git repository")
    parser.add_argument("-o", "--output", default="output.txt", help="Path to the output file")
    parser.add_argument("-i", "--ignore", default=".gptignore", help="Path to the ignore file")

    args = parser.parse_args()

    ignore_file_path = os.path.join(args.repo_path, args.ignore)

    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    with open(args.output, 'w') as output_file:
        output_file.write("The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context.\n")
        process_repository(args.repo_path, ignore_list, output_file)

    with open(args.output, 'a') as output_file:
        output_file.write("--END--")

    print(f"Repository contents written to {args.output}.")

if __name__ == "__main__":
    main()
