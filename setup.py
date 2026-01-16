from setuptools import setup, find_packages

setup(
    name="mdata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "massive",
    ],
    entry_points={
        "console_scripts": [
            "mdata=mdata.cli:main",
        ],
    },
)
