# pyvts
## Overview
`pyvts` is a python library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

You can easily use the library to develop VTubeStudio Plugin to achieve your goals. For example, adding new tracking parameters to enable more actions on live2d avatars.

## Quick Start

### Installation

```
pip3 install pyvts 
```

### Get Started

First import library you need,
```
import pyvts
import asyncio
```

Then specify your plugin information
```
plugin_info = {
    "plugin_name": "[plugin name]",
    "developer": "[your name]",
    "authentication_token_path": "./token.txt",
}
```
Create an instance and do whateveer you want!
```
async def main():
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    # Implement what you want to do
    await vts.close()

if __name__ == "__main__":
    asyncio.run(main())
```


```eval_rst

.. toctree::
   :maxdepth: 2
   :caption: Package Contents:

   README.md
   CONTRIBUTING.md
   pyvts.rst
```