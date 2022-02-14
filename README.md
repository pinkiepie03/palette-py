# palette-py
A simple tool to get color palettes from images

## Dependencies

The script only depends on [color-thief-py](https://github.com/fengsp/color-thief-py). To install it simply
run

> pip install colorthief

## Usage

palette-py is really simple tool, it has just a couple of options.

 - -n: Specify the number of colors you want to extract from the image in question (optional)
 - -i: Specify the path to the image in question (required)

**For example**,

> ./palette.py -i path/to/image.jpg -n 7

will extract a palette of seven colors from the image.jpg

## Contributing to palette-py

Feel free to send me a pull-request if you think some change on the scrip is necessary
