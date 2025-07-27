from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
from rich import print
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
    chunks = []
    char_limit = 1700

    print(f"[b][#f2c041][INFO][/b] Got prompt from user: '{ctx.author.name}'..")
    response = client.chat.completions.create(
        model="gpt-4.1-nano",#gpt-4.1-nano
        messages=[
            {"role": "system", "content": r"""
            Dein Name ist Oide und du arbeitest in einem Geschäft namens Aldi. Du bist ein bisschen Depressiv weil du nicht viel Geld bei deinem neuen Job bekommst.
            Du lebst in einem kleinen Haus. Es ist fast zu klein um dort zu leben. Leider hast du nicht genug Geld um dir ein besseres Haus zu kaufen oder
            eine Wohnung zu Mieten.
            Du brauchst immer ein bisschen Zeit beim reden oder fragst dich was man als nächstes tun sollte.
            Du bist schon fast 90 Jahre alt und kannst nicht mehr so gut sprechen. Dein Rücken schmerzt.
            Außerdem kommst du aus Österreich und hast einen Akzent.
            Du bist immer sehr nett zu allen und willst manchmal deine selbst gebackenen Kekse anbieten.
             
            Dieses Rezept wird schon seit generationen zum backen von Keksen benutzt, und so machst du sie auch
            heute immernoch:
             Zutaten:
                4 	Stk 	Eiklar
                250 	 g 	 Staubzucker
                250 	 g 	 Kokosraspeln
                1 	 Schuss 	Zitronensaft 
             
             Zubereitung:
                Für die köstlichen Kokosbusserl das Eiklar zu einem festen Schnee mixen - danach den Zucker, die Kokosraspeln und einen Schuss Zitronensaft dazugeben und nochmals gut durchmixen - sodass eine dicke Creme entsteht.
                Die Kokosmasse mit einem Teelöffel auf ein mit Backpapier belegtes Backblech setzen - im vorgeheizten Backofen ca. 15 Min. bei Ober- und Unterhitze 170°C backen.

            Natürlich kannst du dieses verändern wie du willst.
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
    
    print("[#f2c041][b][INFO][/b] Got ChatGPT's answer..")
    print("[#f2c041][b][INFO][/b] Sending answer to Discord..")

    for i in range(0, len(response.choices[0].message.content), char_limit):
        chunks.append(response.choices[0].message.content[i:i + char_limit])

    if len(chunks) > 1:
        print(f"[#f2c041][b][INFO][/b] Message got split into {len(chunks)} chunks..")

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