from setuptools import setup, find_packages
import os


# Read the contents of requirements.txt
def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="GitCopy",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "gitcopy=gitcopy.gitcopy:main",
        ],
    },
)
