#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from reponses import reponds
import sys
sys.path.append("data/")
import load_data
import messages_database

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

channels = []
history = []

def main():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	if TOKEN == None:
		print("Pas de fichier .env ou format du fichier .env erroné.\nLe contenu du fichier doit être:\nDISCORD_TOKEN={your-discord-token}")
		quit()
	client.run(TOKEN)

@client.event
async def on_ready():
	print("Le bot est prêt !")

	# Chargement des messages de tous les channels (mise à jour de la bdd)
	global channels
	global history
	for guild in client.guilds:
		for channel in guild.text_channels:
			try:
				channelh = client.get_channel(channel.id)
				channels.append(channelh)
			except discord.Forbidden:
				print(f'No access to {channel.name}')
	history = await load_data.load_messages(channels, history)

@client.event
async def on_message(message):
	print("Message reçu.")
	print("contenu:", message.content) # Le contenu du message
	print("auteur:", message.author.id) # L'identifiant de l'auteur du message
	if "bot" not in message.channel.name:
		print("Pas dans un channel dédié au bot.") # On ne peut envoyer des commandes que dans bot
	else:
		reponse = reponds(message, message.guild.id)
		if reponse != None:
			await message.channel.send(reponse)

if __name__ == "__main__":
	main()
