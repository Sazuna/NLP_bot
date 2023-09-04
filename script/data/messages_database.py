#!/bin/python3


import sqlite3

con = sqlite3.connect("messages.db")

cur = con.cursor()

def create_or_load_table():
	try:
		cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY NOT NULL, channelId TEXT NOT NULL, messageId TEXT NOT NULL, userId TEXT, content TEXT NOT NULL)")
		con.commit()
		return []
	except sqlite3.OperationalError:
		print("Table messages trouvée. Chargement des messages")
		return load_table()

def load_table():
	cur.execute("SELECT * FROM messages")
	res = cur.fetchall()
	return res


def add_message(channelId, messageId, userId, content):
	content = content.replace("'", "%27")
	cur.execute(f"INSERT INTO messages (channelId, messageId, userId, content) VALUES('{channelId}', '{messageId}', '{userId}', '{content}')")
	con.commit()


def get_link(guildId, channelId, messageId):
	return "https://discord.com/channels/{guildId}/{channelId}/{messageId}"

def get_last_saved_message_id(channelId):
	req = f"SELECT messageId, id, content FROM messages WHERE channelId == '{channelId}' and messageId >= (SELECT MAX(messageId) FROM messages WHERE channelId == '{channelId}')"
	cur.execute(req)
	res = cur.fetchall()
	if len(res) > 0:
		return res[0][0]
	else:
		return None
