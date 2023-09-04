#!/bin/python3

#from tfidf import tfidf
from sklearn.feature_extraction.text import TfidfVectorizer
import bao
import messages_database

def preprocess_message(m):
	m = bao.del_urls(m)
	m = bao.lowercase(m)
	m = bao.lemmatize(m)
	m = bao.del_stopwords(m)
	m = bao.del_punct(m)
	m = bao.del_digits(m)
	return m

async def load_messages(channels, messages):
	if len(messages) == 0:
		messages.extend(messages_database.create_or_load_table())
	for channel in channels:
		last_saved_message_id = messages_database.get_last_saved_message_id(channel.id)
		# Get the last message of the current channel using its id
		last_saved_message = None
		if last_saved_message_id != None:
			try:
				last_saved_message = await channel.fetch_message(last_saved_message_id)
			except:
				print("The last saved message ({last_saved_message_id}) in channel {channel.id} hasn't been retrieved.")
				last_saved_message = None

		# Get history starting from the last saved message in our database

		async for message in channel.history(limit=None, after=last_saved_message):
			if len(message.content) >= 1:
				messages.append([-1, message.id, message.author.id, channel.id, message.content])
				messages_database.add_message(channel.id, message.id, message.author.id, message.content)
	return messages
