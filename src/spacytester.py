#!/usr/bin/python

import spacy
nlp = spacy.load('en_core_web_sm')

type(nlp)

doc = nlp("Exposure to air pollution significantly increases the risk of infertility, according to the first study to examine the danger to the general population.")

type(doc)

print(doc)

for token in doc:
    print(token.text, token.lemma, token.lemma_, token.pos_, token.tag_)



if __name__=="__main__":
    #nothing yet?


