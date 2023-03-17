from setuptools import setup, find_packages

setup(
    name="gptswe",
    version="1.0.1",
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
)

