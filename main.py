import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv
from rich import print
from openai_chat import openai_chat

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

class Bot(commands.Bot):
    async def on_ready(self):
        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------")

    async def on_message(self, message: discord.message):
        char_limit = 1900

        if message.author == bot.user:
            return

        if message.channel.id == 1398730068729135337: #Replace with your Channel ID
            chunks = openai_chat(message.content, char_limit)

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
