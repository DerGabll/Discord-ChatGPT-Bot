import discord
import os
from datetime import datetime
from discord.ext import commands 
from dotenv import load_dotenv
from rich import print
from openai_chat import openai_chat

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
CHAR_LIMIT = 1900
MEMORY_FILE = "memory.txt"
OWNER_ID = 1289363432864354365

class Bot(commands.Bot):
    async def delete_messages(self, message: discord.message):
        await message.channel.send("Deleting all Messages..")
        await message.channel.purge(limit=None)
        return

    async def clear_memory(self, message: discord.message):
        with open(MEMORY_FILE, "w") as file:
            file.write("")
        await message.channel.send("Cleared all Chat history", delete_after=2)
        return 

    def is_owner(self, message: discord.message, include_admin: bool=True):
        if not include_admin:
            return message.author.id == OWNER_ID
        else:
            return message.author.guild_permissions.administrator

    async def on_ready(self):
        self.time = f"[white]{datetime.now().strftime('%H:%M')}[white]"
        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------\n")

    async def on_message(self, message: discord.message):
        if message.author == bot.user:
            return
        if message.content == "!clear" and self.is_owner(message):
            await self.delete_messages(message)
            return 
        elif message.content == "!memory" and self.is_owner(message):
            await self.clear_memory(message)
            return 
        elif message.content == "!purgeAll" and self.is_owner(message):
            await self.clear_memory(message)
            await self.delete_messages(message)
            return 

        if message.content.startswith(".ignore"):
            return
            
        if message.channel.id == 1398730068729135337: #Replace with your Channel ID
            chunks = openai_chat(message.content, message.author.display_name, CHAR_LIMIT, MEMORY_FILE, self.time)

            await message.channel.send(f"""‎ \n
```fix

{message.author.display_name}:\n{message.content}```‎\n""")

            for chunk in chunks:
                await message.channel.send(f"""{chunk}""")

            print(f"{self.time} [green][b][SUCCES][/b] Succesfully sent answer to Discord!\n\n")        

            await message.delete()       



intents = discord.Intents.all()
bot = Bot(command_prefix="!", intents=intents)

bot.run(BOT_TOKEN)
