# gptswe

`gptswe` is a command-line tool that converts the contents of a Git repository into a text format readable by large language models like GPT-4.

By default


## Getting Started

```
$ pip install gptswe

$ gptswe -c Fix the bug in the login page and make the logo bigger

1037 tokens copied to the clipboard.
```

Then simply navigate to your favorite AI chat platform, press ctrl+v to paste, and press enter.

When the AI has finished doing your work, copy and paste


## Ignoring Files

Any files listed in `.gitignore` will be ignored by `gptswe`

Additionally, any files listed in `.gptignore` will be ignored (using the same syntax).


## License
Based on `gpt-repository-loader` by [mpoon](https://github.com/mpoon)

This project is licensed under the MIT License - see the LICENSE file for details.

