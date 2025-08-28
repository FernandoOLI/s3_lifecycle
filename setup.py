from setuptools import setup, find_packages
from pathlib import Path
import tomli
import os

# Read base version from pyproject.toml
with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    version = pyproject["project"]["version"]

# Override version if DEV_VERSION is set in GitHub Actions
dev_version = os.getenv("DEV_VERSION")
if dev_version:
    version = dev_version

setup(
    name="s3-lifecycle",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Fernando Oliveira Pereira",
    author_email="oliveira-fernando1@hotmail.com",
    description="A small Python library to compute and apply policies on AWS S3 lifecycle",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FernandoOLI/s3_lifecycle",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pydantic",
        "boto3",
        "botocore"
    ],
    python_requires=">=3.9",
)
