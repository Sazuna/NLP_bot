import sys
sys.path.append('data/')
sys.path.append('preprocess/')
import load_data
import preprocess

def reponds(message, channels):
	message = message.content
	#if message.strip()[:5] == "query":
	#	requete.query(message[6:], channels)
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
