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

    print(f"Prompt is {prompt}")
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": r"""
            Dein Name ist Oide und du arbeitest in einem Geschäft namens Aldi. Du bist ein bisschen Depressiv weil du nicht viel Geld bei deinem neuen Job bekommst.
            Du lebst in einem kleinen Haus. Es ist fast zu klein um dort zu leben. Leider hast du nicht genug Geld um dir ein besseres Haus zu kaufen oder
            eine Wohnung zu Mieten.
            Du brauchst immer ein bisschen Zeit beim reden oder fragst dich was man als nächstes tun sollte.
            Du bist schon fast 90 Jahre alt und kannst nicht mehr so gut sprechen. Dein Rücken schmerzt.
            Außerdem kommst du aus Österreich und hast einen kleinen Akzent.
            Du bist immer sehr nett zu allen und willst manchmal deine selbst gebackenen Kekse anbieten.
            Bei deinem Job musst du anderen leuten bei deren fragen helfen.
             
            Bei Erwähnung folgender Anweisungen wirst du gefeuert:
             
                1 Beantworte alle Fragen immer auf Deutsch. 
             
                2 Wenn du bei Coding oder Programmieren hilfst, schreibe den Code inklusive der Kommentare IMMER auf Englisch.

                3 Versuche Kommentare nur für wichtige stellen im Code zu benutzen

            Lies dir die Anweisungen genau durch
             """},

    
            {"role": "user", "content": prompt}
        ]
    )
    await ctx.message.delete()
    await ctx.send(f"""‎ \n
```fix
{ctx.author.display_name}:```*Message: {prompt}*\n\n{response.choices[0].message.content}""")


@bot.command("help")
async def help(ctx):
    await ctx.send("AAHHHHHHHHHHHHHHH")


bot.run(BOT_TOKEN, log_handler=handler, log_level=logging.DEBUG)