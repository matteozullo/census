from setuptools import setup, find_packages

setup(
    name="census",  # Package name
    version="0.1",
    packages=find_packages(),  # Automatically find packages in the repo
    install_requires=[
        "geopandas",  # Package for geospatial data
        "us",         # Package for US-specific information
        "typing",     # Type hinting library (if needed for compatibility)
    ],  # Add dependencies here
    author="Your Name",
    description="A package for working with Census data",
    url="https://github.com/matteozullo/Census",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
