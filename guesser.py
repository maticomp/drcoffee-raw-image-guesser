import numpy as np
import os
import operator

from scipy import ndimage
from PIL import Image

def get_possible_dimensions(path):
    pixel_count = os.path.getsize(path) / 2

    length_array = np.arange(1, pixel_count)

    widths = length_array[
        np.mod(pixel_count, length_array) == 0
    ]
    widths = widths[
        (widths <= 800) & (widths >= 40)
    ].astype(int)

    combinations = np.dstack(np.meshgrid(widths, widths)).reshape(-1, 2)
    dimensions = combinations[np.prod(combinations, axis=1) == pixel_count]

    return dimensions

def raw_rgb585array_to_imagearray(raw_array, width, height):
    r_array = ((raw_array >> 11) & 0x1f ) << 3
    g_array = ((raw_array >> 5 ) & 0x3f ) << 2
    b_array = ((raw_array      ) & 0x1f ) << 3

    return np.dstack(
        (r_array, g_array, b_array)
    ).reshape(width, height, 3).astype(np.uint8)

def get_filtered_variance(image_array):
    return ndimage.variance(ndimage.median_filter(image_array, 4))

def get_raw_array_from_file(path):
    return np.fromfile(
        path, dtype=np.int16, count=os.path.getsize(path)
    )

def guess_dimensions(path):
    raw_array = get_raw_array_from_file(path)

    variances = {
        (width, height): get_filtered_variance(
            raw_rgb585array_to_imagearray(
                raw_array, width, height
            )
        ) for width, height in get_possible_dimensions(path)
    }

    ((guessed_width, guessed_height), _) = max(
        variances.items(), key=operator.itemgetter(1)
    )

    return guessed_width, guessed_height

def raw_rgb585_to_png(path, width, height):
    filename, extension = os.path.splitext(path)

    image_array = raw_rgb585array_to_imagearray(
        get_raw_array_from_file(path), width, height
    )

    output_filename = f'{filename}.png'

    return output_filename, Image.fromarray(image_array).save(output_filename)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file")

    args = parser.parse_args()

    guessed_width, guessed_height = guess_dimensions(args.input)

    print('Guessed dimensions:', guessed_width, guessed_height)

    output_filename, _ = raw_rgb585_to_png(
        args.input, guessed_width, guessed_height
    )

    print('Written', output_filename)
