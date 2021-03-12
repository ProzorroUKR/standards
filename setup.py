import os
import sys
from setuptools import setup, find_packages

setup(
    name="standards",
    version="1.0.9",
    description="Prozorro standards",
    python_requires=">=2.7",
    package_dir={'standards': '.'},
    package_data={
        'standards': ['*/*'],
    },
    packages=["standards"],
    include_package_data=True,
)
