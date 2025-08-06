import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv
from rich import print
from openai_chat import openai_chat

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
CHAR_LIMIT = 1900
MEMORY_FILE = "memory.txt"

class Bot(commands.Bot):
    async def on_ready(self):
        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------")

    async def on_message(self, message: discord.message):
        if message.author == bot.user:
            return
        if message.content == "!clear":
            with open(MEMORY_FILE, "w") as file:
                file.write("")
            await message.channel.send("CLEARED ALL HISTORY")
            return

        if message.channel.id == 1398730068729135337: #Replace with your Channel ID
            chunks = openai_chat(message.content, CHAR_LIMIT, MEMORY_FILE)

            await message.channel.send(f"""‎ \n
```fix

{message.author.display_name}:\n{message.content}```‎\n""")

            for chunk in chunks:
                await message.channel.send(f"""{chunk}""")

            print("[green][b][SUCCES][/b] Succesfully sent answer to Discord!\n\n")        

            await message.delete()        



intents = discord.Intents.all()
bot = Bot(command_prefix="!", intents=intents)

bot.run(BOT_TOKEN)
