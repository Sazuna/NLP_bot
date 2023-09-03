#!/bin/python3

#from tfidf import tfidf
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
sys.path.insert(1, '../')
import bao

def preprocess_message(m):
	m = bao.del_urls(m)
	m = bao.lowercase(m)
	m = bao.lemmatize(m)
	m = bao.del_stopwords(m)
	m = bao.del_punct(m)
	m = bao.del_digits(m)
	return m

async def load_messages(channels):
	# lire le document avec les messages enregistrés.
	for channel in channels:
		messages = await(channel.history(limit=100, check=check).flatten())
	print(messages)
	return messages

def requete(query):
	messages = load_messages()
	with open ("stopwords.txt", 'r') as stop:
		stopwords = stop.readline().split()
	
	tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                             min_df=0.2, stop_words=stopwords,
                             use_idf=True, tokenizer=tokenize_and_stem, 
ngram_range=(1,3))

def main():
	messages = load_messages	
	requete("bonjour à tous, les amis !")

if __name__ == "__main__":
	main()
