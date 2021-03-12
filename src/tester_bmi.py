#!/usr/bin/python

import os
import sys
import argparse
import numpy as np

############### Argument parsing ###############
# Initialize parser
parser = argparse.ArgumentParser(
    description = "Generates visualization of network, as well as calculates centrality measures for nodes") 

parser.add_argument(
    "-w",
    "--weight",
    type = int,
    default = 80, # Default when not specifying
    required = False, # Since we have a default value, it is not required to specify this argument
    help = "int: weight in kg")

parser.add_argument(
    "-H",
    "--height", 
    type = int,
    default = 180, # Default when not specifying
    required = False, # Since we have a default value, it is not required to specify this argument
    help = "int: height in cm")

args = parser.parse_args()

def bmi(weight, height):
    bmi = weight/np.power((height/100),2)
    print(bmi)

if __name__=="__main__":
    bmi(args.weight, args.height)

