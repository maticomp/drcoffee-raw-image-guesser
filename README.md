# drcoffee-raw-image-guesser

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Simple tool to guess correct image dimensions for Dr. Coffee espresso machine RAW image files

## What and why?

Dr. Coffee espresso machines come with USB connector giving access to mass storage
device on which there is a collection of different `*.bin` files with image
assets used in the machine, e.g. drink icons or screensavers.

Those files are RAW framebuffers with RGB565 color encoding and contain
no metadata whatosever, hence image dimensions are unknown.

While converting RGB 565 RAWs to PNG is possible with different tools,
`ffmpeg` being one of the most obvious, without knowing the image dimensions
it's not possible to get a correct image.

This tool tries to guess the dimensions by trying all sensible combinations,
extracting the image, and applying median blur and calculating color variance
to distinguish between images with defined shapes and noise.

## How to use

### Install requirements

```
pip install -r requirements.txt
```

### Run on any Dr. Coffee image

```
python guesser.py image.bin
```

the command will try to guess the image size and output `image.png` in
the current directory.
