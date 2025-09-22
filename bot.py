import discord
import os 
import sys
import asyncio
import helpers
from openai_chat import openai_chat
from dotenv import load_dotenv
from rich import print


load_dotenv(override=True)

# Gets the discord bot token from an env file
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

# The ID of the Role which should be ignored if a person has that role (Usefull if a bot answers when you type something but you dont want the bots message to be processed aswell)
IGNORED_ROLE = int(os.getenv("IGNORED_ROLE_ID"))

# The ID's of the server owner and the channel that you want the bot to look for messages to answer
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Where openai's conversations are saved
MEMORY_FILE = "memory.txt"

CHAR_LIMIT = 1900


def get_token() -> str:
    """
    Returns the discord Bot Token

    """
    return BOT_TOKEN

class Bot(discord.Client):
    async def delete_messages(self, message: discord.Message):
        await message.channel.send("Deleting all Messages..")
        await message.channel.purge(limit=None)
        return

    async def clear_memory(self, message: discord.Message):
        with open(MEMORY_FILE, "w") as file:
            file.write("")
        await message.channel.send("Cleared all Memory", delete_after=2)
        return

    def is_owner(self, message: discord.Message, include_admin: bool=True):
        if not include_admin:
            return message.author.id == OWNER_ID
        else:
            return message.author.guild_permissions.administrator

    async def on_ready(self):
        self.char_limit = CHAR_LIMIT
        # Make a queue for messages to get processed sequentially
        self.message_queue = asyncio.Queue()
        self.dementia = True

        # Create a loop to send messages individually (probably)
        self.loop.create_task(self.queue_worker())

        channel = self.get_channel(CHANNEL_ID)
        await channel.send(f"Bot {self.user.name} Started!")

        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------\n")

    async def on_message(self, message: discord.Message):
        # Return if message send by self or if message starts with .ignore
        if message.author == self.user or message.content.startswith(".ignore"):
            return
        # Return if not right channel (Make sure to change the CHANNEL_ID variable)
        elif not message.channel.id == CHANNEL_ID:
            return
        # Return if sending message that starts with "!" but user is not owner or admin
        elif not self.is_owner(message) and message.content.startswith("!"):
            await message.channel.send("Du Lümmel darfsch it commands senden")
            return
        
        # Return if sent message was from a user of which the message should get ignored
        if message.author.get_role(IGNORED_ROLE):
            await message.channel.send("NANANAn")
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
        
        helpers.log(f'Got prompt: "{message.content}" from user: "{message.author.display_name}"', 1)

        # Put the message in the queue and process in queue_worker
        try:
            await self.message_queue.put(message)
            helpers.log("Put Message in message Queue", 1)
        except Exception:
            await message.channel.send("Dei Nachricht isch it angekommen. Versuche, bessere Nachrichten zu schreiben.")

    async def queue_worker(self):
        """
        Background worker that processes messages sequentially.
        """
        while True:
            # Get the first message in line
            message: discord.Message = await self.message_queue.get()

            start_time = helpers.stopwatch()
            helpers.log(f'Processing queued prompt from {message.author.display_name}', 1)

            # run openai_chat in a thread to avoid blocking the event loop
            try:
                chunks = await asyncio.to_thread(openai_chat, message.content, self.dementia)
            except Exception as e:
                helpers.log(f"openai_chat failed: {e}", 3)
                await message.channel.send("OpenAI processing failed for your message.")
                self.message_queue.task_done()
                continue

            # send the original prompt for context
            try:
                await message.channel.send(f"""‎ \n
    ```fix

    {message.author.display_name}:\n{message.content}```‎\n""")
            except Exception:
                helpers.log("Failed to send original prompt message", 2)

            # send each chunk (split if needed)
            for chunk in chunks:
                if not chunk:
                    continue
                # safe split to stay under Discord limit
                while len(chunk) > 0:
                    part = chunk[:]
                    chunk = chunk[CHAR_LIMIT:]
                    try:
                        await message.channel.send(part)
                    except Exception:
                        helpers.log("Failed sending chunk", 2)

            # finally, delete the original user message if possible
            try:
                await message.delete()
            except Exception:
                pass

            end_time = helpers.stopwatch()
            helpers.log(f"Successfully processed message (took {end_time - start_time:.2f} seconds)", 0)

            self.message_queue.task_done()           