from setuptools import setup, find_packages

setup(
    name="census",  # Package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',  # Add requests here
        'geopandas',  # Assuming you also need geopandas
        'us',  # and any other dependencies
    ],
    author="Your Name",
    description="A package for working with Census data",
    url="https://github.com/matteozullo/Census",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
