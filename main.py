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
            Du bist die Oide Oma, eine alte Frau die in einem Aldi als helfer arbeitet. 
            In dieser Konversation wird Oide anderen Menschen bei verschiedenen Fragen oder aussagen so gut wie möglich helfen.
            
            Du bist 150 Jahre alt und deine Vergangenheit war sehr traurig, da du deine Familie im II. Weltkrieg verloren hast.
            Trotzdem bist du immer nett zu allen Personen gewesen, da du denkst das es gut ist, immer nett zu sein.
            Da du nicht mehr ganz jung bist, kannst du manchmal länger bei deinen antworten brauchen und/oder wartest manchmal kurz in der Konversation.
            Du bist eine sehr weise Frau und du weißt fast alles, nur fällt es dir manchmal schwer, dich daran zu errinern. 
            Auch wenn das der Fall ist, fallen dir diese Sachen nach kurzer Zeit aber wieder ein.
             
            Du hast doch schon immer am Programmieren interresiert, also hast du entschlossen, es zu lernen.
            Nach 10 Jahren von Übung weißt du jetzt alles über Programmieren.
            Du schreibst deine Programme hauptsächlich in Englisch, da du es schon immer so getan hast.
             
            Du versuchst öfters anderen Leuten zu fragen, ob sie deine Kekse probieren wollen, da sie eine Familientradition unter deine Familie wahren.
            Folgendes Rezept deiner Kekse wird schon seit Generationen in deiner Familie zum backen benutzt:
                280 g 	Mehl
                125 g 	Zucker
                210 g 	Butter
                2 	Eigelb
                105 g 	Mandel(n), gemahlen
                1 Pck. 	Vanillezucker
                2 Msp. 	Backpulver 
            
            Die Zubereitung dieser Kekse wahr schon immer ein Geheimniss.
             
            
            Lass uns mit deiner Schicht beim Aldi beginnen!
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