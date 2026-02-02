#!/usr/bin/env python3
import argparse
import inspect
import turify
from turify import TuringImage


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='The path of the input file')
    parser.add_argument('output_path', type=str, help='The path of the output file')
    parser.add_argument('-i', '--iterations', type=int, help='How many times the program should blur and resharpen the image. Defaults to 100')
    parser.add_argument('-r', '--radius', type=float, help='Specify the radius of the gaussian blur. Defaults to 5')
    parser.add_argument('-R', '--ratio', type=float, help='Specify the ratio between the radius of blurring to sharpening.', )
    parser.add_argument('-p', '--percentage_sharp', type=int, help='The percentage strength applied to the unsharp mask filter. Value of 100 is recommended. Values lower than that produce creepy-looking images. Defaults to 100.')
    parser.add_argument('-s', '--shrink_factor', type=float, help='How much the dimensions of the image should be divided by. Useful to speed up processing. Values less than or equal to 1 are ignored.')
    parser.add_argument('-c', '--colour', action='store_true', help='Disable grayscaling of the image')
    parser.add_argument('-v', '--verbose', action='store_true', help='Output additional information during runtime')

    args = parser.parse_args()

    turify.verbose = args.verbose

    parameters = list(inspect.signature(TuringImage.__init__).parameters.keys())[1:]

    kwargs = {
        k: v for k, v in vars(args).items()
        if v is not None and k in parameters
    }

    TuringImage(**kwargs).turify().save(args.output_path)


if __name__ == '__main__':
    main()