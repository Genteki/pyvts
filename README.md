# pyvts
[![License: MIT](https://img.shields.io/github/license/Genteki/pyvts?style=flat-square)](https://opensource.org/licenses/MIT) [![issue](https://img.shields.io/github/issues/genteki/pyvts?style=flat-square)](https://github.com/Genteki/pyvts/issues) [![build](https://img.shields.io/circleci/build/github/Genteki/pyvts?style=flat-square)](https://circleci.com/gh/Genteki/pyvts)
[![codecov](https://img.shields.io/codecov/c/github/genteki/pyvts?color=informational&style=flat-square)](https://codecov.io/gh/Genteki/pyvts)

A python library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

## Overview
Create a class `VTS` connecting to the server running on VTubeStudio (default port: `ws://localhost:8001`).

Implement functions in `VTS` to send/receive text messages to/from the server, to achieve developers' goals. For example, adding new tracking parameters to enable more actions on live2d avatars.

## Installation

> pip3 install pyvts

## Quick Start
Demo [examples/start.py](./examples/start.py) is a good startpoint to make plugin for VTubeStudio. 

Before you get started, make sure you've installed all the dependcies

> pip3 install -r requirements.txt

Then, launch `VTubeStudio`, and run

> python3 examples/start.py

in command line. You will see a new tracking parameter "start_parameter" added to VTubeStudio and some information about it in command line ouput.