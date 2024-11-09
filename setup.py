from setuptools import setup, find_packages

setup(
    name="GitCopy",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gitcopy=gitcopy.gitcopy:main",
        ],
    },
)
