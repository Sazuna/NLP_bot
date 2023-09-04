#!/bin/python3

import argparse
import sys
import os

import re
import string

import nltk
from nltk.tokenize import word_tokenize

# racinisation (stem)
#from nltk.stem import PorterStemmer # Pour l'anglais
from nltk.stem import SnowballStemmer # Pour le français

# tagger
#from nltk import pos_tag # ne marche pas pour le français
#from nltk.tag import StanfordPOSTagger # tagger du français mais le code est compliqué
import spacy # on est (presque) obligé d'utiliser spacy pour le tagging du français
nlp = spacy.load("fr_core_news_sm")


# Si pas encore téléchargé nltk, décommenter :
# nltk.download('punkt')

stopwords_list = []

# suppression des liens
def del_urls(text):
	return re.sub(r"https?://[a-zA-Z0-9\.\-,/\?:@&=+\$#]*", '', text, re.MULTILINE)

# suppression des chiffres
def del_digits(text):
	return ' '.join([c for c in text if not c.isdigit()])


# tokenisation
def tokenize(text):
	return word_tokenize(text)

# passage en minuscule à l'exception des noms propres
def lowercase(tokens):
	if type(tokens) == list:
		tokens = ' '.join(tokens)
	doc = nlp(tokens)
	return [token.text.lower() if not token.pos_ == "PROPN" else token.text for token in doc]

# suppression des stopwords
def del_stopwords(tokens, stopwords="stopwords.txt"):
	if type(tokens) == str:
		tokens = tokenize(tokens)

	global stopwords_list
	if len(stopwords_list) == 0:
		with open (stopwords, 'r') as stop:
			stopwords_list = stop.readline().split()
	return [token for token in tokens if token not in stopwords_list]


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
	if type(tokens) == str:
		tokens = tokenize(tokens)
	stemmer = SnowballStemmer("french")
	return [stemmer.stem(token) for token in tokens]


# suppression des ponctuations
def del_punct(tokens):
	if type(tokens) == str:
		tokens = tokenize(tokens)
	return [token for token in tokens if token not in string.punctuation]


# ngrams
def n_grams(tokens, n):
	n_grams = []
	for i in range(0, len(tokens) - n):
		n_gram = []
		for j in range (0, n):
			n_gram.append(words[i+j])
		n_grams.append(n_gram)
	return n_grams

def write_ngrams(output_file, ngrams):
	with open(output_file, "w") as f:
		for ngram in ngrams:
			f.write(','.join(ngram) + '\n')

def main(input_file, args):
	with open (input_file, "r") as f:
		text = f.read().strip()
	if args.url == 1:
		text = del_urls(text)
	if args.lowercase == 1:
		text = lowercase(text)

	if args.lemmatize == 1:
		text = lemmatize(text)
	elif args.stemmatize == 1:
		text = stem(text)

	# ponctuation et stopwords sont à enlever en dernier car les IA ont besoin de ces informations pour le lowercase, la lemmatisation etc.
	if args.stopwords != None:
		text = del_stopwords(text, args.stopwords)
	if args.punct == 1:
		text = del_punct(text)
	if args.digits == 1:
		text = del_digits(text)

	if args.ngram != None:
		ngrams = n_grams(text, int(args.ngram[0]))
		ngrams_output = "ngrams_output.txt"
		if len(args.ngram) > 1:
			ngrams_output = args.ngram[1]
		write_ngrams(ngrams_output, ngrams)
	print(text)


# Main function
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", type=str, help="Input file", required=True)
	parser.add_argument("-s", "--stopwords", type=str, nargs='?', const="stopwords.txt", help="Stopwords file path if stopwords should be removed")
	parser.add_argument("-n", "--ngram", type=str, nargs='+', help="If conversion to ngrams is needed and how many.\n\t -n ngram_num [ngrams_output_file]")
	parser.add_argument("-l", "--lowercase", help="To lowercase", action="store_const", const=1)
	parser.add_argument("-p", "--punct", help="Remove punctuation", action="store_const", const=1)
	parser.add_argument("-d", "--digits", help="Remove digits", action="store_const", const=1)
	parser.add_argument("-u", "--url", help="Remove urls", action="store_const", const=1)

	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument("-L", "--lemmatize", help="Lemmatize", action="store_const", const=1)
	group.add_argument("-S", "--stemmatize", help="Stemmatize", action="store_const", const=1)

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)		
	if not os.path.exists(args.input):
		print(f"Input file {args.input} does not exist.")
		sys.exit(0)
	if args.stopwords != None and not os.path.exists(args.stopwords):
		print(f"Stopwords file {args.stopwords} does not exist.")
		sys.exit(0)
	#
	# Program
	#
	main(args.input, args)
