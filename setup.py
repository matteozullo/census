from setuptools import setup, find_packages

setup(
    name="census",  # Package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',  # For making HTTP requests
        'geopandas',  # For geographic data processing
        'us',  # For handling US state data
        'pandas',  # For data manipulation
    ],
    author="Your Name",
    description="A package for working with Census data",
    url="https://github.com/matteozullo/Census",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
