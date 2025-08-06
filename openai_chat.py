from dotenv import load_dotenv
from openai import OpenAI
from rich import print
from roles import roles
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_HISTORIES = 5

client = OpenAI(api_key=OPENAI_API_KEY)

def openai_chat(prompt, char_limit, memory_file):
    chunks = []
    role = roles("ASSISTANT")

    print(f"[b][#f2c041][INFO][/b] Got prompt")

    if not os.path.exists(memory_file):
        with open(memory_file, "x"):
            pass

    with open(memory_file, "r") as file:
        memory = file.readlines()

    response = client.chat.completions.create(
        model="gpt-4.1-nano",#gpt-4.1-nano
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": f"""{prompt}\n\nHier ist dein Chatverlauf zwischen dem User und dir. Jede Frage ist so Aufgebaut: 
    REQUEST FROM USER: 
    <request>
    RESPONSE FROM CHATGPT: 
    <response>

Hier ist der Chatverlauf: 
    {memory}

Schaue dir den Verlauf gut an und antworte immer mit einbeziehung des Chatverlaufs
            """}
        ]
    )

    openai_response = response.choices[0].message.content

    with open(memory_file, "r") as file:
        lines = file.readlines()

    with open(memory_file, "a") as file:
        user_request = "REQUEST FROM USER:"
        history_count = 0
        
        file.write(f"""
{user_request} 
{prompt}
RESPONSE FROM CHATGPT: 
{openai_response}
        """)

        for line in lines:
            if line.startswith(user_request):
                history_count += 1
        print(f"[#f2c041][b][INFO][/b] There are currently {history_count} conversations in memory")

        while history_count >= MAX_HISTORIES:
            with open(memory_file, "r") as file:
                lines = file.readlines()
            
            with open(memory_file, "w") as file:
                count = 0

                for line in lines:
                    if line.startswith(user_request):
                        count += 1
                    
                    if count >= 2:
                        file.write(line)
            history_count -= 1

        

    
    print("[#f2c041][b][INFO][/b] Got ChatGPT's answer..")
    print("[#f2c041][b][INFO][/b] Sending answer to Discord..")

    for i in range(0, len(openai_response), char_limit):
        chunks.append(openai_response[i:i + char_limit])

    if len(chunks) > 1:
        print(f"[#f2c041][b][INFO][/b] Message got split into {len(chunks)} chunks..")

    return chunks
