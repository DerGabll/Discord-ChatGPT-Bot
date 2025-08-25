from dotenv import load_dotenv
from openai import OpenAI
from roles import roles, log
from datetime import datetime
import os

load_dotenv()

# Your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# How many conversations should be kept in the memory file while dementia is enabled
MAX_CONVERSATIONS = 5

# The personality of the Bot
ROLE_NAME = "NICE_GRANDMA" # Look at roles.py for roles to choose or add

client = OpenAI(api_key=OPENAI_API_KEY)

def openai_chat(prompt: str, char_limit: int, memory_file: str, dementia: bool):
    chunks = []

    role = roles(ROLE_NAME, memory_file) or "" # Checks if role exists else makes it have no prompt

    # Create memory file if it doesnt exist
    if not os.path.exists(memory_file):
        with open(memory_file, "x"):
            pass
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano", # Best model because of speed and roleplay. gpt-5 isn't very good at acting
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )

    openai_response = response.choices[0].message.content

    with open(memory_file, "a") as file:
        user_request = "REQUEST FROM USER:"
        file.write(f"""{user_request} 
{prompt}
RESPONSE FROM CHATGPT: 
{openai_response}\n\n""")

    with open(memory_file, "r") as file:
        lines = file.readlines()

    count: int = 0

    for line in lines:
        count += 1 if line.startswith(user_request) else 0 # Get all conversations

    # Limit the amount of conversations in memory if dementia is turned on
    if dementia:
        with open(memory_file, "w") as file:
            for line in lines:      
                if count >= MAX_CONVERSATIONS:
                    count -= 1 if line.startswith(user_request) else 0

                if count < MAX_CONVERSATIONS:
                    file.write(line)            

    log(f"There are currently {count + 1} conversations in memory", 1)
    log("Got ChatGPT's answer and sending it to Discord..", 1)

    for i in range(0, len(openai_response), char_limit):
        chunks.append(openai_response[i:i + char_limit])

    if len(chunks) > 1:
        log(f"Message got split into {len(chunks)} chunks", 1)

    return chunks