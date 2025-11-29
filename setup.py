#!/usr/bin/env python3
"""
Setup script for CoreX
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="corex",
    version="1.0.0",
    author="CoreX Team",
    author_email="hello@corex.dev",
    description="A comprehensive Django scaffolding framework for rapid application development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramazon07-cmd/corex",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Framework :: Django",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "corex=corex.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "corex": ["templates/**/*", "templates/industry/**/*"],
    },
)
