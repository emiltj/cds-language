#!/usr/bin/python

# Write the following in your terminal/bash, when you are within the correct folder
# python collocation.py ../data/100_english_novels/corpus/ cart 1

#Importing all the necessary modules
import os
import re
import numpy as np
from collections import *
import pandas as pd
from pathlib import Path
from os import *
import re
import io
import os
import numpy as np
from collections import Counter
from collections import defaultdict
import pandas as pd
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Retrieves collocates for a given keyword in a given directory within a given window, and outputs a csv. with information')
parser.add_argument('text_dir', type=str, help='directory of texts')
parser.add_argument('keyword', type=str, help='keyword')
parser.add_argument('window_size', type=int, help='size of window (number indicates the number of tokens before and after the keyword')
args = parser.parse_args()

# Define function which includes the arguments text directory, keyword and window size (the latter n-words before and n-words after keyword)
def collocation(text_dir, keyword, window_size = 1):
    # Make a list that the loop appends to
    collocations = list()
    collocations_unique = list()
    concordance_lines = list()
    collocate_lines = list()
    n_collocate_occurences = list()
    N = 0

    # For each file in the filepath that ends with .txt, read the file into "text"
    for file in Path(text_dir).glob("*9.txt"):
        with open(file, "r", encoding="utf-8") as file:
            text = file.read()

            # Tokenize each text into individual words
            text_tokens = re.compile(r"\W+").split(text)
            N += len(text_tokens)
            
            # Return index for each element text_tokens if the element in text_tokens is equal to keyword
            indices = [index for index, match in enumerate(text_tokens) if match == keyword]
            
            # For each keyword in the text, create an object (= concordance_line) that has keyword and the words just before and after (keyword +- window_size)
            for index in indices:
                concordance_line = text_tokens[max(0,index - window_size):index+window_size+1]
                
                # Append the concordance line to "concordance_lines"
                concordance_lines.append(concordance_line)

                # For each word in the concordance_line, add it to "new_collocations" if it is not the keyword.
                new_collocations = [collocate for collocate in concordance_line if collocate != keyword]

                # For each word in the concordance_line, add it to "new_collocations_unique" if it is not the keyword and if it does not already exist in the list.
                new_collocations_unique = [collocate for collocate in concordance_line if collocate not in collocations_unique and collocate != keyword]
                
                # Extend my list collocations, with all the collocations (words around keyword)
                collocations.extend(new_collocations)
                
                # Extend my list collocations_unique, with all the collocations (words around keyword) that do not already appear in the list.
                if new_collocations_unique not in collocations_unique:
                    collocations_unique.extend(new_collocations_unique)
    
    # o21 # n-times collocate occurs w/o keyword (same as: n(collocate) minus o11)
    for file in Path(text_dir).glob("*9.txt"):
        with open(file, "r", encoding="utf-8") as file:
            text = file.read()

            # Tokenize each text into individual words
            text_tokens = re.compile(r"\W+").split(text)

            #
            for unique_collocate in collocations_unique:
                indices = [i for i, x in enumerate(text_tokens) if x == unique_collocate]
                n_collocate_occur = {unique_collocate : len(indices)}
                n_collocate_occurences.append(n_collocate_occur)
    
    # Define dictionary to loop into
    n_collocate_dict = Counter({})

    #
    for dic in n_collocate_occurences:
        # If dictionary is empty
        if bool(n_collocate_dict) == False:
            n_collocate_dict = Counter(dic)
        dic = Counter(dic)
        n_collocate_dict = n_collocate_dict + dic
    
    # Go through the collocations (all words that have appeared with the keyword in any of the texts) and count how often they have occured with the keyword.
    o11 = Counter(collocations)

    # o21 # n-times collocate occurs w/o keyword (same as: n(collocate) minus o11)
    o21 = n_collocate_dict - o11

    # Create an empty dictionary for counting concordance lines where keyword occurs without collocation.
    o12 = dict()
    
    # For each unique collocation in collocations_unique:
    for collocation_unique in collocations_unique:
        
        # Set loop counter
        loop_count = 0
        
        # For each line in concordance_lines, if the unique collocation does NOT appear, add +1 to counter
        for concordance_line in concordance_lines:
            if collocation_unique not in concordance_line:
                loop_count += 1

        # Updating the o12 to include a count for n-times that each unique collocation did not appear with a keyword
        o12.update({collocation_unique : loop_count})
    
    # Getting number of concordance lines (and we have 1 per keyword)
    n_times_keyword = len(concordance_lines)
    
    # Writing a dictionary with the keys for all collocates, and the value for n_keywords.
    R1 = Counter({x: n_times_keyword for x in o12})

    # Calculating C1:
    C1 = o11 + o21 # C1 # n-times collocate occurs (regardless of keyword) (same as o11 + o21)
    
    # Calculating E11:
    # We know the formula: (R1*C1)/N, 
    # #Therefore we first calculate R1*C1:
    R1_multiplied_with_C1 = {k: R1[k]*C1[k] for k in R1} # Dictionary comprehension for multiplying values between dictionaries for the same keys
    # Then we multiply each of the key-value pairs with N. This gets us E11
    E11 = Counter({k:v/N for (k,v) in R1_multiplied_with_C1.items()})

    # Calculating MI
    # We know the formula: log(o11/e11)
    # First we then divide o11 with e11
    o11_divided_by_E11 = {k: o11[k] / float(E11[k]) for k in E11 if k in o11}
    # Then we take the log of each to get MI-scores
    MI = {k:np.log(v) for (k,v) in o11_divided_by_E11.items()}

    # Create a pandas to write
    df_mi = pd.DataFrame.from_dict(MI, orient="index",
                    columns=["mi"])
    df_raw_freq = pd.DataFrame.from_dict(o11, orient="index",
                    columns=["raw_freq"])
    
    df = df_mi.join(df_raw_freq)
    df['collocate'] = df.index
    df.reset_index(drop=True, inplace=True)
    df = df[['collocate', 'raw_freq', 'mi']]
    
    # Create path for output file
    outpath = os.path.join(".", f"{keyword}_collocations_info.csv")
    df.to_csv(outpath)
    
    print(f"A new file has been created: {outpath}")

    #print(f"N-times collocates occurs in the text (regardless of keyword): {n_collocate_dict}")
    #print(f"All concordance lines with keyword: {concordance_lines}")
    #print(f"All collocations (not unique): {collocations}")
    #print(f"All unique collocations: {collocations_unique}")
    #print(f"Number of collocations: {len(collocations)}")
    #print(f"Number of unique collocations: {len(collocations_unique)}")
    #print(f"Number of tokens, total: {N}") # # N # Number of words (or sum of C1 + C2 or sum of R1 + R2)
    #print(f"Raw frequency - N-times keyword occurs with collocate: {o11}") # Raw-frequency! (n-times keyword occurs with collocate)
    #print(f"N-times keyword occurs w/o collocate: {o12}") # n-times keyword occurs w/o collocate
    #print(f"N-times keyword occurs (regardless of collocate): {R1}") # n-times keyword occurs (regardless of collocate)
    #print(f"N-times collocates occurs w/o keyword: {o21}") # o21 # n-times collocate occurs w/o keyword (same as: n(collocate) minus o11)
    #print(f"N-times collocates occurs (regardless of keyword): {C1}") # C1 # n-times collocate occurs (regardless of keyword) (same as o11 + o21)
    #print(f"E11 (Expected frequency, given the total frequency of the keyword + collocates): {E11}")
    #print(f"MI): {MI}") # MI's for all collocates
# If called from the command line(terminal) (if namespace is = main, then:)
if __name__=="__main__":
    collocation(args.text_dir, args.keyword, args.window_size)