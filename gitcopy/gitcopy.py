import argparse
import os
import shutil
import sys
import tempfile

import pyperclip
from git import InvalidGitRepositoryError, Repo


def main():
    parser = argparse.ArgumentParser(
        description="Copy all scripts from a Git repository into a single text file."
    )
    parser.add_argument(
        "repo_url",
        help="URL of the GitHub repository or '.' for the current repository",
    )
    parser.add_argument(
        "-y", "--yank", action="store_true", help="Copy the output to the clipboard"
    )
    args = parser.parse_args()

    repo_url = args.repo_url
    yank = args.yank

    if repo_url == ".":
        # Use the current directory as the repository root
        try:
            repo = Repo(os.getcwd(), search_parent_directories=True)
            temp_dir = repo.working_tree_dir
        except InvalidGitRepositoryError:
            print(
                "Error: The current directory is not a Git repository.", file=sys.stderr
            )
            sys.exit(1)
        repo_name = os.path.basename(os.path.abspath(temp_dir))
        cleanup = False  # No need to clean up the current directory
    else:
        # Create a temporary directory to clone the repo
        temp_dir = tempfile.mkdtemp()
        cleanup = True
        try:
            # Clone the repository
            print(f"Cloning repository {repo_url}...")
            Repo.clone_from(repo_url, temp_dir)
            repo = Repo(temp_dir)
        except Exception as e:
            print(f"Failed to clone repository {repo_url}: {e}", file=sys.stderr)
            shutil.rmtree(temp_dir)
            sys.exit(1)
        # Get the repository name
        repo_name = os.path.basename(repo_url.rstrip("/"))
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

    output_filename = f"{repo_name}.md" if not yank else "output.md"

    # Initialize the output content with the prompt
    prompt_text = (
        "The following text is a Git repository with code. The structure of the text are "
        "sections that begin with ----, followed by a single line containing the file "
        "path and file name, followed by a variable amount of lines containing the file "
        "contents. The text representing the Git repository ends when the symbols --END-- "
        "are encounted. Any further text beyond --END-- are meant to be interpreted as "
        "instructions using the aforementioned Git repository as context.\n\n"
    )
    output_content = [prompt_text]

    # Get the list of tracked files
    tracked_files = repo.git.ls_files().split("\n")

    # Process each tracked file
    for rel_path in tracked_files:
        file_path = os.path.join(temp_dir, rel_path)
        # Read the content of the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            output_content.append(f"----\n# {rel_path}\n{content}")
        except Exception as e:
            print(f"Could not read file {rel_path}: {e}", file=sys.stderr)

    # Append --END-- to signify the end of the repository content
    output_content.append("--END--")

    # Combine the output content
    final_output = "\n".join(output_content)

    if yank:
        pyperclip.copy(final_output)
        print("Output copied to clipboard.")
    else:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"Output written to {output_filename}")

    if cleanup:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
