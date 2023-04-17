#!/bin/python3
import discord
import os
from dotenv import load_dotenv

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
	print(message.content)
	if message.content == "Ping":
		await message.channel.send("Pong")
	

if __name__ == "__main__":
	main()
