#!/usr/bin/python

# Importing all the necessary modules
from collections import Counter
from itertools import combinations
from tqdm import tqdm
import os
import sys
import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load("en_core_web_sm")

############### Argument parsing ###############
# Initialize parser
parser = argparse.ArgumentParser(
    description = "Generates visualization of network, as well as calculates centrality measures for nodes") 

# Add parser arguments
parser.add_argument(
    "-e",
    "--edgelist", 
    type = str,
    default = os.path.join("..","data","weighted_edgelist.csv"), # Default when not specifying a path
    required = False, # Since we have a default value, it is not required to specify this argument
    help = "str containing path to edgelist file")

parser.add_argument(
    "-n",
    "--n", 
    type = int,
    default = 30, # Default when not specifying anything in the terminal
    required = False, # Since we have a default value, it is not required to specify this argument
    help = "int specifying number of node + edge pairs wanted in the analysis (top n weighted pairs")
args = parser.parse_args()

parser.add_argument(
    "-s",
    "--save", 
    type = bool,
    default = True, # Default when not specifying 
    required = False, # Since we have a default value, it is not required to specify this argument
    help = "bool specifying whether to save visualization and centrality measures")

args = parser.parse_args()


def network_analysis(edgelist, n, save):
    # Load in the edgelist
    weighted_edgelist = pd.read_csv(edgelist, index_col = 0)

    # Get only the n strongest connections
    weighted_edgelist = weighted_edgelist.sort_values(by=['weight'], ascending = False, na_position='last').iloc[0:n,:]

    # Create a graph from the edgelist
    G = nx.from_pandas_edgelist(weighted_edgelist, 'nodeA', 'nodeB', ["weight"])

    # Plot
    nx.draw_shell(G, with_labels = True, font_weight= 'bold') 

    # Calc centrality measures
    ev = pd.DataFrame(nx.eigenvector_centrality(G).items(), columns=['node', 'eigenvector_centrality'])
    bc = pd.DataFrame(nx.betweenness_centrality(G).items(), columns=['node', 'betweenness_centrality'])
    dg = pd.DataFrame(nx.degree_centrality(G).items(), columns=['node', 'degree_centrality'])

    # Make into a df
    ev = ev.merge(bc, on = "node")
    centrality_measures = ev.merge(dg, on = "node")


    # Save plot and df of centrality measures
    if save == True:
        # Save the centrality measures in the folder "output" (and create the folder if it doesn't already exist)
        output_folder = os.path.join("..", "data", "output")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, "centrality_measures.csv")
        centrality_measures.to_csv(output_path)

        # Save the horrible plot in the folder "viz"  (and create the folder if it doesn't already exist)
        viz_folder = os.path.join("..", "data", "viz")
        if not os.path.exists(viz_folder):
            os.makedirs(viz_folder)
        viz_plot = os.path.join(viz_folder, "network_viz.png")
        plt.savefig(viz_plot, dpi=300, bbox_inches="tight")

        print(f"A new visualization has been created: {output_path} \nA new file with centrality measures has been created: {viz_plot}")

if __name__=="__main__":
    network_analysis(args.edgelist, args.n, args.save)

