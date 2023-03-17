from setuptools import setup, find_packages

setup(
    name="gptrepo",
    version="1.2.1",
    packages=find_packages(),
    install_requires=[
        'pathspec',
        'gptwc',
        ],
    entry_points={
        "console_scripts": [
            "gptrepo=gptrepo.gptrepo:main",
        ]
    },
)

