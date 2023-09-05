#!/bin/python3

import preprocess

import sqlite3

con = sqlite3.connect("messages.db")

cur = con.cursor()

def create_or_load_table():
	try:
		cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY NOT NULL, channelId TEXT NOT NULL, messageId TEXT NOT NULL, userId TEXT, content TEXT NOT NULL, processed TEXT)")
		con.commit()
		return []
	except sqlite3.OperationalError:
		print("Table messages trouvée. Chargement des messages.")
		return load_table()

def load_table():
	cur.execute("SELECT * FROM messages")
	res = cur.fetchall()
	return res

def load_processed():
	cur.execute("SELECT id, processed FROM messages WHERE processed IS NOT NULL AND LENGTH(processed) > 0")
	res = cur.fetchall()
	return res


def add_message(channelId, messageId, userId, content):
	content = content.replace('"', "%22")
	content = content.replace("'", "%27")
	cur.execute(f"INSERT INTO messages (channelId, messageId, userId, content) VALUES('{channelId}', '{messageId}', '{userId}', '{content}')")
	con.commit()


def get_link(guildId, id_):#channelId, messageId):
	cur.execute(f"SELECT channelId, messageId, content FROM messages WHERE id = {id_}")
	res = cur.fetchall()
	if (len(res) == 0):
		return f"Message n°{id_} not found in database."
	channelId = res[0][0]
	messageId = res[0][1]
	#content = rem_process(res[0][2])
	return f"https://discord.com/channels/{guildId}/{channelId}/{messageId}"#\n{content}"

def get_last_saved_message_id(channelId):
	req = f"SELECT messageId, id, content FROM messages WHERE channelId == '{channelId}' and messageId >= (SELECT MAX(messageId) FROM messages WHERE channelId == '{channelId}')"
	cur.execute(req)
	res = cur.fetchall()
	if len(res) > 0:
		return res[0][0]
	else:
		return None

def add_processed(id_, text):
	text = text.replace('"', "%22")
	text = text.replace("'", "%27")
	cur.execute(f"UPDATE messages SET processed = '{text}' WHERE id = {id_}")
	con.commit()

def rem_process(text):
	text = text.replace("%22", '"')
	text = text.replace("%27", "'")
	return text

def preprocess_database():
	req = "SELECT * FROM messages WHERE processed IS NULL"
	cur.execute(req)
	res = cur.fetchall()
	for entry in res:
		m = preprocess.preprocess_message(entry[4])
		add_processed(entry[0], m)
