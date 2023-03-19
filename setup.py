from setuptools import setup, find_packages

setup(
    name="gptswe",
    version="1.2.3",
    packages=find_packages(),
    install_requires=[
        'pathspec',
        'gptwc',
        ],
    entry_points={
        "console_scripts": [
            "gptswe=gptswe.gptswe:main",
        ]
    },
    author="Larry Neal",
    author_email="nealla@lwneal.com",
    description="A command-line tool that converts Git repositories into a text format readable by GPT-4 and copies it to your clipboard",
    license="MIT",
    url="https://github.com/lwneal/gptswe",
)

