import sys
sys.path.append('data/')
sys.path.append('preprocess/')
sys.path.append('search_engine/')
import load_data
import preprocess
import search

def reponds(message, guildId):
	message = message.content
	if message.strip()[:5] == "query":
		return search.query(message[6:], guildId)
	if message.strip()[:10] == "preprocess":
		return preprocess.preprocess_message(message[10:].strip())
	if message == "j'en ai marre":
		return "moi aussi :("
	if message == "Ping":
		return "Pong"
	if message == "pierre":
		return "feuille. perdu :)"
	if message == "feuille":
		return "ciseaux. dommage :/"
	if message == "ciseaux":
		return "pierre. raté!"
	if message == "puits":
		return "couvercle !"
