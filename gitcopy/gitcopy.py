import argparse
import os
import tempfile
import shutil
import sys
from git import Repo
import pyperclip


def main():
    parser = argparse.ArgumentParser(
        description="Copy all scripts from a GitHub repository into a single text file."
    )
    parser.add_argument("repo_url", help="URL of the GitHub repository")
    parser.add_argument(
        "-y", "--yank", action="store_true", help="Copy the output to the clipboard"
    )
    args = parser.parse_args()

    repo_url = args.repo_url
    yank = args.yank

    # Create a temporary directory to clone the repo
    temp_dir = tempfile.mkdtemp()
    try:
        # Clone the repository
        print(f"Cloning repository {repo_url}...")
        Repo.clone_from(repo_url, temp_dir)

        # Get the repository name
        repo_name = os.path.basename(repo_url)
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        output_filename = f"{repo_name}.txt" if not yank else "output.txt"

        # Initialize the output content
        output_content = []
        output_content.append(
            "The following text is a Git repository with code. The structure of the text are "
            "sections that begin with ----, followed by a single line containing the file "
            "path and file name, followed by a variable amount of lines containing the file "
            "contents. The text representing the Git repository ends when the symbols --END-- "
            "are encountered. Any further text beyond --END-- are meant to be interpreted as "
            "instructions using the aforementioned Git repository as context.\n"
        )

        # Get the list of tracked files
        repo = Repo(temp_dir)
        tracked_files = repo.git.ls_files().split("\n")

        # Define script extensions
        script_extensions = [
            ".py",
            ".sh",
            ".bat",
            ".js",
            ".rb",
            ".pl",
            ".ps1",
            ".php",
            ".java",
            ".c",
            ".cpp",
            ".h",
            ".cs",
            ".go",
            ".swift",
            ".kt",
            ".rs",
            ".ts",
            ".lua"
        ]

        # Process each tracked file
        for rel_path in tracked_files:
            file_path = os.path.join(temp_dir, rel_path)
            _, ext = os.path.splitext(file_path)
            if ext.lower() in script_extensions:
                # Read the content of the file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    output_content.append(f"----\n{rel_path}\n{content}")
                except Exception as e:
                    print(f"Could not read file {rel_path}: {e}", file=sys.stderr)

        # End of the repository representation
        output_content.append("--END--\n")

        # Combine the output content
        final_output = "\n".join(output_content)

        if yank:
            pyperclip.copy(final_output)
            print("Output copied to clipboard.")
        else:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(final_output)
            print(f"Output written to {output_filename}")

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
