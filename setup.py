from setuptools import setup, find_packages

setup(
    name="gpt-repository-loader",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gpt_repository_loader = gpt_repository_loader:main",
        ]
    },
)

