from setuptools import setup, find_packages

setup(
    name="mdata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "massive",
        # pandas, pyarrow, numpy are assumed to be in the environment (Colab)
        # but listing them here for completeness if users install elsewhere
        "pandas",
        "pyarrow",
    ],
    entry_points={
        "console_scripts": [
            "mdata=mdata.cli:main",
        ],
    },
)
