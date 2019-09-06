from pathlib import Path
from setuptools import setup, find_packages

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PySandbox",
    version="0.3.0",
    packages=find_packages(),
    url="https://github.com/isidentical/pysandbox",
    description="Safe evaluation of untrusted code on containers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['docker'],
)
