from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deproto",
    version="0.2.3",
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
)
