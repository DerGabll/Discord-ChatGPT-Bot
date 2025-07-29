from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
from rich import print
from openai_chat import chat
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

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"[blue][b]Bot {bot.user.name} Started!")
    print("[blue][b]------------------------------------")

@bot.command("chat")
async def ask_openai(ctx, *, prompt: str):
    char_limit = 1700
    chunks = chat(ctx, prompt, char_limit)    

    await ctx.send(f"""‎ \n
```fix
{ctx.author.display_name}:\n{prompt}```‎\n""")
    
    for i in range(len(chunks)):
        await ctx.send(f"""{chunks[i]}""")
    
    print("[green][b][SUCCES][/b] Succesfully sent answer to Discord!\n\n")        

    await ctx.message.delete()


@bot.command("help")
async def help(ctx):
    await ctx.send("AAHHHHHHHHHHHHHHH")


bot.run(BOT_TOKEN, log_handler=handler, log_level=logging.DEBUG)
