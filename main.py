from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
from rich import print
import interactions
import discord
import logging
import os

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True 

bot = interactions.Client(token=BOT_TOKEN, intents=intents)


bot.start()
