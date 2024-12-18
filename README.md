# GitCopy

**GitCopy** is a Python CLI tool to extract all tracked scripts from a GitHub repository into a single text file, with each script prefixed by its relative path.

## Installation

```bash
pip install git+https://github.com/samleeney/GitCopy.git
```

## Usage

Save all scripts to a text file named after the repository:

```bash
gitcopy <repository_url>
```

Copy the output directly to your clipboard:

```bash
gitcopy <repository_url> -y
```

Copy the entire repository from the root directory or subdirectories:

```bash
gitcopy .
```

Open the output file in a text editor defined by the `$EDITOR` environment
variable:

```bash
gitcopy <repository_url> -e
```

## Example

```bash
gitcopy https://github.com/psf/requests
```

Output saved as `requests.txt`:

```
The following text is a Git repository with code. The structure of the text are 
sections that begin with ----, followed by a single line containing the file 
path and file name, followed by a variable amount of lines containing the file 
contents. The text representing the Git repository ends when the symbols --END--
are encounted. Any further text beyond --END-- are meant to be interpreted as 
instructions using the aforementioned Git repository as context.

=== requests/api.py ===
import requests

def get(url, **kwargs):
    return requests.request("GET", url, **kwargs)

...
```

## Requirements

- Python 3.7+
- `GitPython` and `pyperclip` (installed automatically)
- Git CLI tool (`git --version` should work)

For clipboard support on Linux, install `xclip` or `xsel`.
