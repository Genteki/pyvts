# pyvts

[![License: MIT](https://img.shields.io/github/license/Genteki/pyvts?style=flat-square)](https://opensource.org/licenses/MIT) [![issue](https://img.shields.io/github/issues/genteki/pyvts?style=flat-square)](https://github.com/Genteki/pyvts/issues) [![build](https://img.shields.io/circleci/build/github/Genteki/pyvts?style=flat-square)](https://circleci.com/gh/Genteki/pyvts)
[![codecov](https://img.shields.io/codecov/c/github/genteki/pyvts?color=informational&style=flat-square)](https://codecov.io/gh/Genteki/pyvts)
[![PyPI](https://img.shields.io/pypi/v/pyvts?style=flat-square)](https://pypi.org/project/pyvts/)
[![docs](https://img.shields.io/badge/docs-passing-success?style=flat-square)](https://genteki.github.io/pyvts)

A python library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

## Overview

`pyvts` is a python library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

You can easily use the library to develop VTubeStudio Plugin to achieve your goals. For example, adding new tracking parameters to enable more actions on live2d avatars.

## Quick Start

### Installation

```shell
pip3 install pyvts 
```

### Get Started

First import library you need,

```python
import pyvts
import asyncio
```

Create an instance with default values, and do whateveer you want!

```python
async def main():
    vts = pyvts.vts()
    await vts.connect()
    # Implement what you want to do
    await vts.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Demo

Demo [examples/start.py](./examples/start.py) is a good startpoint to make plugin for VTubeStudio. 

Before you get started, make sure you've clone the library and installed all the dependcies

```python
pip3 install -r requirements.txt 
```

Then, launch `VTubeStudio`, and run

```python
python3 examples/start.py 
```

in command line. You will see a new tracking parameter "start_parameter" added to VTubeStudio and some information about it in command line ouput.
