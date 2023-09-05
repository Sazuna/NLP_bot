from sklearn.feature_extraction.text import TfidfVectorizer
import tfidf
from preprocess import preprocess_message
from messages_database import preprocess_database
from messages_database import load_processed
from messages_database import get_link

X = None
messages = []

def query(query, guildId):
	q = preprocess_message(query).split(' ')
	print("query : ", q)

	global messages
	preprocess_database() # preprocess non-processed messages
	if len(messages) == 0:
		messages = load_processed() # refresh messages var at each use of the command

	all_tfidf = [0]*10
	msg_id = [0]*10
	tfidf_min = 0
	idx_min = 0

	historyIdx = [(m[0], m[1]) for m in messages if m[1] != None and m[1].strip() != ''] #To keep a track on the index of each message
	history = [m[1] for m in historyIdx] # Only the messages

	for message in historyIdx:
		tfidf_w = 0
		for word in q:
			#m = preprocess.preprocess_message(message[4]).split(' ')
			tfidf_w += tfidf.tfidf(word, message[1], history)
		# 10 highest tfidfs
		if tfidf_w > tfidf_min: # if better than the top 10, replace the worst tfidf
			all_tfidf[idx_min] = tfidf_w
			msg_id[idx_min] = message[0]
			tfidf_min, idx_min = idx_min_tfidf(all_tfidf)
	return result_string(msg_id, all_tfidf, guildId)

# min and index of min of a list
def idx_min_tfidf(all_tfidf):
	min_ = min(all_tfidf)
	idx = all_tfidf.index(min_)
	return (min_, idx)


# It has to return the links within the classment of best tfidfs, also can show the tfidfs to the users (inside the string), and can show the message itself.
def result_string(msg_ids, all_tfidf, guildId):
	res = ""
	zipped = zip(all_tfidf, msg_ids)
	print(zipped)
	zipped = sorted(zipped, key=lambda x: x[0], reverse=True)
	"""
	for i, msg_id in enumerate(msg_ids):
		link = get_link(guildId, msg_id)
		
		res += "\nscore tfidf:" + str(all_tfidf[i])
		res += "\nlink:" + link
	"""
	for tfidf, msg_id in zipped:
		if tfidf == 0:
			continue
		link = get_link(guildId, msg_id)
		res += "\nscore tfidf:" + str(round(tfidf,2))
		res += "\n\tlink:" + link
	print(res)
	return res
