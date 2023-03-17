# gptswe (the GPT Software Engineer)

`gptswe` is a command-line tool that converts the contents of a Git repository into a text format readable by large language models like GPT-4, adds a prompt telling the AI what to do, and copies the whole thing into your clipboard so you can paste it into a [chat window](https://chat.openai.com/chat).


## Installation

```
$ pip install gptswe
```

## Usage

```
$ gptswe "Fix the bug in the login page and make the logo bigger" -c

1037 tokens copied to the clipboard.
```

Then simply navigate to your favorite AI chat platform, press ctrl+v to paste, and press enter.

When the AI has finished doing your work for you, follow its instructions and copy and paste its generated code back into your text editor as needed.


## Committing

Run the command again with `-m | sh` to automatically generate a commit message crediting GPT-4 as the author (and yourself as the reviewer).

```
$ gptswe "Fix the bug in the login page and make the logo bigger" -m | sh

[main b495a79] Prompt: Fix the bug in the login page and make the logo bigger
 Author: GPT-4 <gpt4@openai.com>
 1 file changed, 20 insertions(+), 1 deletion(-)

```

## Features

If no instructions are provided, `gptswe` will default to the prompt `Identify and fix any obvious bugs in a terse but elegant style. Output a brief explanation of each fix.`

By default, `gptswe` will warn if your total input (files plus prompt) is over 4097 tokens (the limit for GPT-3.5-turbo). Adjust this limit with `--max-tokens`

Output to stdout (default), to a file (using `-o output.txt`) or directly to the clipboard (using `-c`). Uses `pyperclip` for clipboard access.


## An Important Message From GPT-4

As GPT-4, I want to remind you that with great power comes great responsibility. While `gptswe` offers a convenient way to utilize large language models like me in your software development process, it's essential to use this tool responsibly and ethically.

Keep in mind that AI-generated code might have unexpected results, and it's crucial to review and test the output thoroughly before integrating it into your project. Additionally, be mindful of potential biases in the AI's suggestions, and strive to create inclusive, accessible, and secure software.

Lastly, ensure that you comply with all applicable laws, regulations, and ethical guidelines when using AI-generated code in your projects. The future of AI is in your hands – let's build it responsibly together.

- GPT-4


## Example Repository

Visit the [gpt-pong](https://github.com/lwneal/gpt-pong) repository for an example of a project built entirely using the `gptswe` tool.


## Ignoring Files

Any files listed in `.gitignore` will be ignored by `gptswe`

Additionally, any files listed in `.gptignore` will be ignored (using the same syntax).


## License
Based on `gpt-repository-loader` by [mpoon](https://github.com/mpoon)

This project is licensed under the MIT License - see the LICENSE file for details.

