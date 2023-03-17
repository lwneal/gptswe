# gptrepo

`gptrepo` is a command-line tool that converts the contents of a Git repository into a text format, preserving the structure of the files and file contents. The generated output can be interpreted by AI language models, allowing them to process the repository's contents for various tasks, such as code review or documentation generation.

## Getting Started

```
pip install gptrepo

gptrepo
```

## Ignoring Files

Any files listed in `.gitignore` will be ignored by `gptrepo`

Additionally, any files listed in `.gptignore` will be ignored (using the same syntax).


## License
Based on `gpt-repository-loader` by mpoon

This project is licensed under the MIT License - see the LICENSE file for details.

