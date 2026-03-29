import discord
import bot
from dotenv import load_dotenv

load_dotenv(override=True) # override to make sure it doesnt take you 2 hours to find out why it doesnt work

# Your Discord Bot token
DISCORD_BOT_TOKEN = bot.get_token()

intents = discord.Intents.all()
bot = bot.Bot(intents=intents)

bot.run(DISCORD_BOT_TOKEN)
