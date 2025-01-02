"""Setup script for deproto."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deproto",
    version="0.2.5",
    author="Ijaz Ur Rahim",
    author_email="ijazkhan095@gmail.com",
    description="A decoder for Google Maps protobuf format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrDebugger/deproto",
    packages=find_packages(),
    maintainer="Ijaz Ur Rahim",
    maintainer_email="ijazkhan095@gmail.com",
    project_urls={
        "Website": "https://ijazurrahim.com",
        "Source": "https://github.com/MrDebugger/deproto",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-cov>=6.0.0",
            "flake8>=7.1.1",
            "black>=24.10.0",
            "isort>=5.13.2",
            "pre-commit>=4.0.1",
        ],
    },
)
