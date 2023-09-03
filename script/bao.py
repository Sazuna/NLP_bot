#!/bin/python3

import argparse
import re
import sys
import os
import string

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
#from nltk import pos_tag # ne marche pas pour le français
#from nltk.tag import StanfordPOSTagger # tagger du français
from nltk.stem import SnowballStemmer

import spacy # on est obligé d'utiliser spacy pour le tagging du français
nlp = spacy.load("fr_core_news_sm")


# Si pas encore téléchargé nltk, décommenter :
# nltk.download('punkt')

# tokenisation
def tokenize(text):
	return word_tokenize(text)

# passage en minuscule à l'exception des noms propres
def lowercase(tokens):
	if type(tokens) == list:
		tokens = ' '.join(tokens)
	doc = nlp(tokens)
	for token in doc:
		print(token.text, token.pos_)
	lower = [token.text.lower() if not token.pos_ == "PROPN" else token.text for token in doc]
	return lower

# lemmatisation (utilisation de spacy)
# à noter que la fonction doc(nlp) est appelée dans lowercase aussi.
# ce n'est pas très optimal si les deux fonctions sont appelées.

# La lemmatisation semble plus adaptée à la plupart des problèmes, car elle garde les majuscules des noms propres.
def lemmatize(tokens):
	if type(tokens) == list:
		tokens = ' '.join(tokens)
	doc = nlp(tokens)
	return [token.lemma_ for token in doc]

# racinisation
# Attention, la racinisation supprime les majuscules des noms propres. Cela veut dire que si on racinise, pas besoin d'appeler la fonction lowercase.
def stem(tokens):
	stemmer = SnowballStemmer("french")
	return [stemmer.stem(token) for token in tokens]

# suppression des stopwords
def del_stopwords(tokens):
	with open ("stopwords.txt", 'r') as stop:
		stopwords = stop.readline().split()
	return [token for token in tokens if token not in stopwords]


# suppression des liens

# suppression des ponctuations
def del_punct(tokens):
	return [token for token in tokens if token not in string.punctuation]


def main():
	text = "Bonjour à tous ! Je m'appelle Liza. Enchantée."
	tokens = tokenize(text)
	no_stop = del_stopwords(tokens)
	print(no_stop)
	no_punct = del_punct(no_stop)
	print(no_punct)

	tokens = tokenize(text)
	lowers = lowercase(tokens)
	print(lowers)
	lemma = lemmatize(lowers)
	print(lemma)
	stems = stem(lowers)
	print(stems)


if __name__ == "__main__":
	main()
