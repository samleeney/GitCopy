# GitCopy

**GitCopy** is a Python CLI tool to extract all tracked scripts from a GitHub repository into a single text file, with each script prefixed by its relative path.

## Installation

```bash
pip install git+https://github.com/yourusername/GitCopy.git
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

## Example

```bash
gitcopy https://github.com/psf/requests
```

Output saved as `requests.txt`:

```
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
