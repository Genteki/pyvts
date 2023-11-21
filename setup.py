"""A python library for interacting with the VTube Studio API"""

from setuptools import setup, find_packages

DESCRIPTION = "A python library for interacting with the VTube Studio API"
VERSION = "v0.3.2"

setup(
    name="pyvts",
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="vtubestudio",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    author="Genteki Zhang",
    author_email="zhangkaiyuan.null@gmail.com",
    url="https://github.com/Genteki/pyvts",
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=["websockets>=10.4", "aiofiles>=23.1.0", "opencv-python>=4.4.0"],
)
