#!/usr/bin/env python

import math
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('height', type=float, help='height of cylinder')
parser.add_argument('radius', type=float, help='radius of cylinder')
args = parser.parse_args()

def cylinder_volume (height, radius = 2):
    pi = math.pi    # more accurate representation of Pi using pythons math library
    volume = height * pi * radius ** 2  # Creates a variable with volume value
    print(volume)   # prints out the volume
    return volume   # returns the volume

# If called from the command line(terminal) (if namespace is = main, then:)
if __name__=="__main__":
    cylinder_volume(args.height, args.radius)