# pyvts
[![License: MIT](https://img.shields.io/github/license/Genteki/pyvts?style=flat-square)](https://opensource.org/licenses/MIT) [![issue](https://img.shields.io/github/issues/genteki/pyvts?style=flat-square)](https://github.com/Genteki/pyvts/issues) [![build](https://img.shields.io/circleci/build/github/Genteki/pyvts?style=flat-square)](https://circleci.com/gh/Genteki/pyvts)
[![codecov](https://img.shields.io/codecov/c/github/genteki/pyvts?color=informational&style=flat-square)](https://codecov.io/gh/Genteki/pyvts)

A python library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

## Overview
Create a class `VTS` connecting to the server running on VTubeStudio (default port: `ws://localhost:8001`).

Implement functions in `VTS` to send/receive text messages to/from the server, to achieve developers' goals. For example, adding new tracking parameters to enable more actions on live2d avatars.