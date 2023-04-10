"""A python library for interacting with the VTube Studio API"""

from setuptools import setup, find_packages
import pyvts

DESCRIPTION = "A python library for interacting with the VTube Studio API"
VERSION = pyvts.__version__

setup(
    name="pyvts",
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="vtubestudio",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    author="Genteki Zhang",
    author_email="zhangkaiyuan.null@gmail.com",
    url="https://github.com/Genteki/pyvts",
    license="MIT",
    packages=find_packages(where="pyvts", exclude=["tests.*", "tests"]),
    install_requires=["websockets", "aiofile"],
)
