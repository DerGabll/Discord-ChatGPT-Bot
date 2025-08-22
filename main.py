import discord
import os
from datetime import datetime
from discord.ext import commands 
from dotenv import load_dotenv
from rich import print
from openai_chat import openai_chat
import sys

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
CHAR_LIMIT = 1900
MEMORY_FILE = "memory.txt"
OWNER_ID = 1289363432864354365
CHANNEL_ID = 1398730068729135337 #Replace with your Channel ID

class Bot(commands.Bot):
    async def delete_messages(self, message: discord.message):
        await message.channel.send("Deleting all Messages..")
        await message.channel.purge(limit=None)
        return

    async def clear_memory(self, message: discord.message):
        with open(MEMORY_FILE, "w") as file:
            file.write("")
        await message.channel.send("Cleared all Memory", delete_after=2)
        return 

    def is_owner(self, message: discord.message, include_admin: bool=True):
        if not include_admin:
            return message.author.id == OWNER_ID
        else:
            return message.author.guild_permissions.administrator

    async def on_ready(self):
        self.dementia = True

        channel = self.get_channel(CHANNEL_ID)
        await channel.send(f"Bot {self.user.name} Started!")

        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------\n")

    async def on_message(self, message: discord.message):
        self.time = f"[white]{datetime.now().strftime('%H:%M')}[white]"

        # Return if message send by self or if message starts with .ignore
        if message.author == bot.user or message.content.startswith(".ignore"):
            return
        # Return if not right channel (Make sure to change the CHANNEL_ID variable)
        elif not message.channel.id == CHANNEL_ID:
            return
        # Return if sending message that starts with "!" but user is not owner or admin
        elif not self.is_owner(message) and message.content.startswith("!"):
            await message.channel.send("Du Lümmel kansch it commands senden leider")
            return

        # Commands
        match message.content:
            case "!clear_chat":
                await self.delete_messages(message)
            case "!clear_memory":
                await self.clear_memory(message)                    
            case "!clear_all":
                await self.clear_memory(message)
                await self.delete_messages(message)
            case "!dementia":
                self.dementia = not self.dementia
                await message.channel.send(f"Dementia now set to: {self.dementia}")
            case "!restart":
                await message.channel.send("Restarting Bot...")
                os.execv(sys.executable, ['python'] + sys.argv)
            case "!stop":
                await message.channel.send("Bot has been stopped")
                quit()
        
        # Main message processing (Sending message to OpenAI - OpenAI processing / sending message - user receiving feedback from OpenAI)
        chunks = openai_chat(message.content, message.author.display_name, CHAR_LIMIT, MEMORY_FILE, self.time, self.dementia)

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
