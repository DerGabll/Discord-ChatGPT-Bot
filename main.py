import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
from rich import print
from openai_chat import openai_chat


load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")
GUILD_ID = discord.Object(1327336293809524828)

client = OpenAI(api_key=API_KEY)

class Bot(commands.Bot):
    async def on_ready(self):
        try:
            guild = discord.Object(1327336293809524828)
            synced = await self.tree.sync(guild=guild)
            print(f"Succesfully synced {len(synced)} Commands from {self.user.name} to guild {guild.id}!")
            
        except Exception as e:
            print(f"Could not sync commands with Discord: {e}")

        print(f"[blue][b]Bot {self.user.name} Started!")
        print("[blue][b]------------------------------------")



intents = discord.Intents.all()
bot = Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="chat", description="Chat with OpenAI's gpt4.1 nano model", guild=GUILD_ID)
async def chat(interaction: discord.Interaction, prompt: str):
    char_limit = 1700

    await interaction.response.defer()

    chunks = openai_chat(interaction, prompt, char_limit)

    # Combine the prompt and the response chunks
    header = f"""‎\n```fix\n{interaction.user.display_name}:\n{prompt}```‎\n"""
    response = header + "\n".join(chunks)

    await interaction.followup.send(response)
    print("[green][b][SUCCESS][/b] Successfully sent answer to Discord!\n\n")

bot.run(BOT_TOKEN)
