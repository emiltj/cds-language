#!/usr/bin/python

# Importing all the necessary modules
import os
import sys
import argparse
import pandas as pd
from collections import Counter
from itertools import combinations 
from tqdm import tqdm
import spacy
nlp = spacy.load("en_core_web_sm")
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)

# Argument parser for terminal use:
parser = argparse.ArgumentParser(
    description = "Generates edgelist from input file") 
parser.add_argument(
    "input_file", 
    type = str, 
    default = os.path.join("..", "data", "labelled_data", "fake_or_real_news.csv"), # Default when not specifying a path
    nargs='?', # Is needed if you want to specify that you don't have to set the arguments (since we have a default)
    help = "Input file for generating edgelist")
args = parser.parse_args()

# Main function of this script
def generate_weighted_edgelist(input_file):
    data = pd.read_csv(input_file)

    real_df = data[data["label"]=="REAL"]["text"]
    real_df = real_df.sample(100)

    text_entities = []

    for text in tqdm(real_df):
        # create temporary list 
        tmp_entities = []
        # create doc object
        doc = nlp(text)
        # for every named entity
        for entity in doc.ents:
            # if that entity is a person
            if entity.label_ == "PERSON":
                # append to temp list
                tmp_entities.append(entity.text)
        # append temp list to main list
        text_entities.append(tmp_entities)

    edgelist = []
    # iterate over every document
    for text in text_entities:
        # use itertools.combinations() to create edgelist
        edges = list(combinations(text, 2))
        # for each combination - i.e. each pair of 'nodes'
        for edge in edges:
            # append this to final edgelist
            edgelist.append(tuple(sorted(edge)))

    counted_edges = []
    for key, value in Counter(edgelist).items():
        source = key[0]
        target = key[1]
        weight = value
        counted_edges.append((source, target, weight))

    edges_df = pd.DataFrame(counted_edges, columns=["nodeA", "nodeB", "weight"])

    outpath = os.path.join("..", "data", "weighted_edgelist.csv")
    edges_df.to_csv(outpath, sep=",", encoding='utf-8', header = True)
    print(f"A new file has been created <{outpath}>")

if __name__=="__main__":
    generate_weighted_edgelist(args.input_file)