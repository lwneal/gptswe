from setuptools import setup, find_packages

setup(
    name="gptrepo",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        'pathspec',
        ],
    entry_points={
        "console_scripts": [
            "gptrepo=gptrepo.gptrepo:main",
        ]
    },
)

