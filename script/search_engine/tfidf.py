#!/bin/python3

from math import log
from nltk.tokenize import word_tokenize

def tfidf(word, doc, corpus):
	tf = doc.count(word)
	if tf == 0:
		return 0 # shortcut to only compute score for messages containing the word
	N = len(doc)
	df = 0
	for text in corpus:
		if word in text:
			df += 1
	w = tf * log(N / df)
	return w

def test():
	corpus = ['This is the first document.',
	'This document is the second document.',
	'And this is the third one.', 
	'Is this the first document?' ,
	'This document is last.']
	# prétraitement: tokenization etc
	for idx, text in enumerate(corpus):
		text = text.lower()
		text = word_tokenize(text)
		corpus[idx] = text
	print(corpus)
	tfidf_ = tfidf('this', corpus[0], corpus)
	print(tfidf_)

if __name__ == "__main__":
	test()
