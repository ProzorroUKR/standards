from glob import glob
from setuptools import setup


setup(
    name="standards",
    version="1.0.188",
    description="Prozorro standards",
    python_requires=">=2.7",
    package_dir={'standards': '.'},
    package_data={
        'standards': glob("*/**/*.json", recursive=True)
    },
    packages=["standards"],
    include_package_data=True,
)
