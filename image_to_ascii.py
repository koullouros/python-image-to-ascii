import argparse
import numpy as np
from PIL import Image, ImageEnhance

# credit for ramps: http://paulbourke.net/dataformats/asciiart/
grey_ramp_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
grey_ramp_2 = " .:-=+*#%@"[::-1]

def value_to_ascii(character_map, value):
    """ Converts a grayscale value in the range of [0, 255] to an ascii equivalent """
    max_value = len(character_map)
    value_idx = int(max_value/255 * value)-1
    return character_map[value_idx]

def get_average(nparray):
    """ Calculate the average of a tile """
    return np.average(nparray)

def image_to_ascii(image, contrast=1, columns=200, tile_height_scale=0.43, gray_character_ramp=None, output_file=None):
    """
    Takes an image and converts it into ascii art.

    :param image: The input image.
    :param contrast: The amount to contrast. Default is 1.
    :param columns: The number of ascii characters per row.
    :param tile_height_scale: Tile scaling for proportions.
    :param gray_character_ramp: The grayscale character ramp to use.
    :param output_file: The file to save the results to. If None, will output to console.
    :return:
    """
    if gray_character_ramp is None:
        # gray scale values from http://paulbourke.net/dataformats/asciiart/
        gray_character_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    image = ImageEnhance.Contrast(Image.open(image).convert('L')).enhance(contrast)

    # the the image dimensions
    width, height = image.size[0], image.size[1]

    # calculate tile width and height
    # tile width depends on specified number of columns
    tile_width = width / columns

    # because text is usually longer than the width, we adjust for that using the
    # tile_height_scale variable
    tile_height = int(tile_width / tile_height_scale)
    rows = int(height / tile_height)

    np_image = np.array(image)

    ascii_image = []
    for row_idx in range(rows):
        row_start = int(row_idx * tile_height)
        row_end = int(row_start + tile_height)
        if row_end > np_image.shape[0]:
            row_end = int(np_image.shape[0])

        current_col = []
        for col_idx in range(columns):
            column_start = int(col_idx * tile_width)
            column_end = int(column_start + tile_width)
            if column_end > np_image.shape[1]:
                column_end = int(np_image.shape[1])

            tile_average = get_average(np_image[row_start:row_end, column_start:column_end])
            current_col.append(value_to_ascii(gray_character_ramp, tile_average))
        ascii_image.append(current_col)

    if output_file is not None:
        with open(output_file, "w", encoding='utf-8') as f:
            f.write('\n'.join([''.join(i) for i in ascii_image]))
    else:
        print('\n'.join([''.join(i) for i in ascii_image]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_image", help="The image to convert to ascii.")
    parser.add_argument("--contrast", dest="contrast", required=False, default=1, type=float,
                        help="The contrast of the greyscaled image to use. Adjusting the value might result in " \
                             "clearer results.")
    parser.add_argument("-s", "--scale", dest="scale", required=False, default=0.43, type=float,
                        help="The vertical height scaling of the tiles used to split the image. If uncertain " \
                        "keep to default.")
    parser.add_argument("-c", "--columns", dest="columns", required=False, default=80, type=int,
                        help="The number of columns the output should be (number of characters per row).")
    parser.add_argument("-o", "--output", dest="output", required=False,
                        help="The file to store the output in. If not specified, will output to console.")
    parser.add_argument("-g", "--greyscale", dest="greyscale_ramp", required=False, default=1, type=int,
                        help="The greyscale ramp mapping to use. Default option (1) uses 70 levels, option 2 " \
                        "uses 10 levels.")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true",
                        help="If set, will reverse the greyscale ramp.")

    args = parser.parse_args()

    ramp_choice = None
    if args.greyscale_ramp == 1:
        ramp_choice = grey_ramp_1
    elif args.greyscale_ramp == 2:
        ramp_choice = grey_ramp_2

    if args.reverse:
        ramp_choice = ramp_choice[::-1]

    image_to_ascii(args.input_image, contrast=args.contrast, columns=args.columns,
                   tile_height_scale=args.scale, gray_character_ramp=ramp_choice, output_file=args.output)

if __name__ == "__main__":
    main()
