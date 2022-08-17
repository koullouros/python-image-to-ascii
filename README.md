# python-image-to-ascii
A python script to convert images to ascii art.

# Usage:
The script can be run from the command line as follows:
```
image_to_ascii.py [-h] [--contrast CONTRAST] [-s SCALE] [-c COLUMNS] [-o OUTPUT] input_image

positional arguments:
  input_image           The image to convert to ascii.

optional arguments:
  -h, --help            show this help message and exit
  --contrast CONTRAST   The contrast of the grayscaled image to use. Adjusting the value might result in clearer results.
  -s SCALE, --scale SCALE
                        The vertical height scaling of the tiles used to split the image. If uncertain keep to default.
  -c COLUMNS, --columns COLUMNS
                        The number of columns the output should be (number of characters per row).
  -o OUTPUT, --output OUTPUT
                        The file to store the output in. If not specified, will output to console.
```

The script can also be imported, you can use the image_to_ascii function as needed.

# Requirements:
```
Pillow~=9.2.0
pip~=21.3.1
wheel~=0.37.1
numpy~=1.23.2
setuptools~=60.2.0
```

# How it works:

1. The script first converts the image into grayscale.
2. The image is split into tiles. Since text is usually taller than wider, the scale value is used to scale the tile height according to the tile width. The tile width depends on the number of columns specified (the number of columns is the number of ascii characters per row).
3. Each tile is averaged and an ascii character is chosen according to this value. This depends on an ascii grayscale color ramp.

The default ascii grayscale color ramp is:
```
"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. "
Credit: http://paulbourke.net/dataformats/asciiart/
```
