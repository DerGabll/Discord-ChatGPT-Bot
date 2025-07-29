from dotenv import load_dotenv
from openai import OpenAI
from rich import print
from roles import roles
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def openai_chat(interaction, prompt, char_limit):
    chunks = []
    role = roles("NICE_GRANDMA")

    print(f"[b][#f2c041][INFO][/b] Got prompt from user: '{interaction.user.name}'..")
    response = client.chat.completions.create(
        model="gpt-4.1-nano",#gpt-4.1-nano
        messages=[
            {"role": "system", "content": role + f"\nDu bist in einer Konversation mit {interaction.user.display_name}:"},
            {"role": "user", "content": prompt}
        ]
    )
    
    print("[#f2c041][b][INFO][/b] Got ChatGPT's answer..")
    print("[#f2c041][b][INFO][/b] Sending answer to Discord..")

    for i in range(0, len(response.choices[0].message.content), char_limit):
        chunks.append(response.choices[0].message.content[i:i + char_limit])

    if len(chunks) > 1:
        print(f"[#f2c041][b][INFO][/b] Message got split into {len(chunks)} chunks..")

    return chunks
