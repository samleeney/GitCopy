import argparse
import os
import shutil
import sys
import tempfile

import pyperclip
from git import Repo


def main():
    parser = argparse.ArgumentParser(
        description="Copy all scripts from a GitHub repository into a single markdown file."
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

        output_filename = f"{repo_name}.md" if not yank else "output.md"

        # Initialize the output content
        output_content = []

        # Get the list of tracked files
        repo = Repo(temp_dir)
        tracked_files = repo.git.ls_files().split("\n")

        # Define script extensions and their corresponding languages
        script_extensions = {
            ".py": "python",
            ".sh": "bash",
            ".bat": "batch",
            ".js": "javascript",
            ".rb": "ruby",
            ".pl": "perl",
            ".ps1": "powershell",
            ".php": "php",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "cpp",
            ".cs": "csharp",
            ".go": "go",
            ".swift": "swift",
            ".kt": "kotlin",
            ".rs": "rust",
            ".ts": "typescript",
            ".lua": "lua",
        }

        # Process each tracked file
        for rel_path in tracked_files:
            file_path = os.path.join(temp_dir, rel_path)
            _, ext = os.path.splitext(file_path)
            if ext.lower() in script_extensions:
                language = script_extensions[ext.lower()]
                # Read the content of the file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    output_content.append(f"### {rel_path}\n")
                    output_content.append(f"```{language}\n{content}\n```")
                except Exception as e:
                    print(f"Could not read file {rel_path}: {e}", file=sys.stderr)

        # Combine the output content
        final_output = "\n\n".join(output_content)

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
