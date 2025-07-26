from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
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

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is running!")

@bot.command("chat")
async def ask_openai(ctx, *, prompt: str):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    await ctx.send(response.choices[0].message.content)

@bot.command("help")
async def help(ctx):
    await ctx.send("AAHHHHHHHHHHHHHHH")


bot.run(BOT_TOKEN, log_handler=handler, log_level=logging.DEBUG)