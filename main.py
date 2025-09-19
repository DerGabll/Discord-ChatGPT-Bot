import discord
import os
from datetime import datetime
from dotenv import load_dotenv
from rich import print
from openai_chat import openai_chat
from roles import log
import sys

load_dotenv(override=True) # override to make sure it doesnt take you 2 hours to find out why it doesnt work
# Your Discord Bot token
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

# Check if BOT_TOKEN loading has an error
if not BOT_TOKEN:
    log("BOT_TOKEN is empty", 3) # Send an error message
    quit()

# At which point openai's answer will get split into another message (keep under ~2000 because you can't send a message over that length)
CHAR_LIMIT = 1900

# Where openai's conversations are saved
MEMORY_FILE = "memory.txt"

# The ID's of the server owner and the channel that you want the bot to look for messages to answer
OWNER_ID = 1289363432864354365
CHANNEL_ID = 1398730068729135337 # Replace with your Channel ID

def get_time():
    return int(datetime.now().strftime('%S'))

class Bot(discord.Client):
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
        await channel.send(f"Bot {self.user.name} Started!", delete_after=2)

        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------\n")

    async def on_message(self, message: discord.message):
        # Return if message send by self or if message starts with .ignore
        if message.author == bot.user or message.content.startswith(".ignore"):
            return
        # Return if not right channel (Make sure to change the CHANNEL_ID variable)
        elif not message.channel.id == CHANNEL_ID:
            return
        # Return if sending message that starts with "!" but user is not owner or admin
        elif not self.is_owner(message) and message.content.startswith("!"):
            await message.channel.send("Du Lümmel darfsch it commands senden")
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

        if message.content.startswith("!"):
            return

        start_time = get_time()
        log(f'Got prompt: "{message.content}" from user: "{message.author.display_name}"', 1)
        # Main message processing (Sending message to OpenAI - OpenAI processing / sending message - user receiving feedback from OpenAI)
        chunks = openai_chat(message.content, CHAR_LIMIT, MEMORY_FILE, self.dementia)

        await message.channel.send(f"""‎ \n
```fix

{message.author.display_name}:\n{message.content}```‎\n""")

        for chunk in chunks:
            await message.channel.send(chunk)

        end_time = get_time()
        log(f"Succesfully sent answer to Discord! (took {end_time - start_time} seconds)\n", 0)

        await message.delete()

intents = discord.Intents.all()
bot = Bot(intents=intents)

bot.run(BOT_TOKEN)
