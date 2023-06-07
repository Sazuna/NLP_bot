#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from reponses import reponds

intents = discord.Intents.all()
client = discord.Client(intents=intents)#intents=discord.Intents.default())

def main():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	print(TOKEN)
	if TOKEN == None:
		print("Pas de fichier .env ou format du fichier .env erroné.\nLe contenu du fichier doit être:\nDISCORD_TOKEN={your-discord-token}")
		quit()
	client.run(TOKEN)

@client.event
async def on_ready():
	print("Le bot est prêt !")

@client.event
async def on_message(message):
	print("Message reçu.")
	print(message.content) # Le contenu du message
	print(message.author.id) # L'identifiant de l'auteur du message
	#print(message.reference.message_id) # L'identifiant du message cité
	reponse = reponds(message.content)
	if reponse != None:
		await message.channel.send(reponse)
	

if __name__ == "__main__":
	main()
