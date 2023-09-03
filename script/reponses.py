import sys
sys.path.insert(1, 'recherche_message/')
import requete

def reponds(message):
	if message.strip()[:5] == "query":
		ir.query(message[6:])
	if message.strip()[:10] == "preprocess":
		return requete.preprocess_message(message[10:].strip())
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
