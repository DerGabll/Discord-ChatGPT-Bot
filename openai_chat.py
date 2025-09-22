from dotenv import load_dotenv
from openai import OpenAI
import helpers
import os
import yaml

load_dotenv(override=True) # override to make sure it doesnt take you 2 hours to find out why it doesnt work

# --------------------
# MAIN OPENAI SETTINGS
# --------------------

# Your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# At which point openai's answer will get split into another message (keep under ~2000 because you can't send a message over that length)
CHAR_LIMIT = 1900

# Where to store the chatlog of OpenAI
MEMORY_FILE = "memory.txt"

# Everything about the role file
ROLE_FILE = "roles.yaml"
ROLE_NAME = "NICE_GRANDMA"

# How many conversations should be kept in the memory file while dementia is enabled
MAX_CONVERSATIONS = 5

client = OpenAI(api_key=OPENAI_API_KEY)

def openai_chat(prompt: str, dementia: bool):
    chunks = []

    # Create memory file if it doesnt exist
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "x"):
            pass

    # Read the yaml file and get the role from the ROLE_NAME file
    with open(ROLE_FILE, "r", encoding="utf-8") as file:
        roles = yaml.safe_load(file)["ROLES"]
        role = roles[ROLE_NAME]

    response = client.chat.completions.create(
        model="gpt-4.1-nano", # Best model because of speed and roleplay. gpt-5 isn't very good at acting 
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )

    openai_response = response.choices[0].message.content

    with open(MEMORY_FILE, "a") as file:
        user_request = "REQUEST FROM USER:"
        file.write(f"""
        {user_request} 
            {prompt}
            RESPONSE FROM CHATGPT: 
            {openai_response}\n\n""".strip()
        )

    with open(MEMORY_FILE, "r") as file:
        lines = file.readlines()

    count: int = 0

    for line in lines:
        count += 1 if line.startswith(user_request) else 0 # Get all conversations

    # Limit the amount of conversations in memory if dementia is turned on
    if dementia:
        with open(MEMORY_FILE, "w") as file:
            for line in lines:      
                if count >= MAX_CONVERSATIONS:
                    count -= 1 if line.startswith(user_request) else 0

                if count < MAX_CONVERSATIONS:
                    file.write(line)            

    helpers.log(f"There are currently {count + 1} conversations in memory", 1)
    helpers.log("Got ChatGPT's answer and sending it to Discord..", 1)

    for i in range(0, len(openai_response), CHAR_LIMIT):
        chunks.append(openai_response[i:i + CHAR_LIMIT])

    if len(chunks) > 1:
        helpers.log(f"Message got split into {len(chunks)} chunks", 1)

    return chunks

if __name__ == "__main__":
    openai_chat("I am a horse. Yee Haw", True)