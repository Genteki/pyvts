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
pip install pyvts 
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

To see more examples, you could visit [tutorial](https://genteki.github.io/pyvts/toctree2_tutorial.html) in documentation.

## Contributing

Contribution is welcome. Please follow the guide of [CONTRIBUING.md](CONTRIBUTING.md).
