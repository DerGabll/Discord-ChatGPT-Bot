# ChatGPT Discord Bot
This is a Discord bot (or app) that you can use to chat with openai's gpt4.1 nano model in a discord server using a command.

# The Setup
### Installing required packages
Copy "main.py" and "requirements.txt" into the same directory. Then open up a console and install the necessary packages using pip:
```pip install -r requirements.txt```
or any other package manager

## Setting up API Key and Discord Token

If you do not have or know where to find the OpenAI API Key, there is a tutorial for that [here](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327).
Same with the Discord Token, [here](https://discordpy.readthedocs.io/en/stable/discord.html) (Make sure that the bot gets the "send messages" permission or just Administrator)

Otherwise, you have two choices when setting up your API Keys:

### API Keys using System environment variables

You will have to setup two system environment variables: DISCORD_TOKEN and OPENAI_API_KEY. If you don't know how to set up environment variables, you can see a tutorial [here](https://pureinfotech.com/create-custom-environment-variables-windows-10/). The values of the Token and Key should each be the token and the key that you got from discord and openai.

### API Keys using .env files

First, make a .env file in the directory with the main.py file. In this file you should write the following text:
```
DISCORD_TOKEN=your_token
```
```
OPENAI_API_KEY=your_api_key
```
where "your_token" and "your_api_key" should be replaced with your Discord Token and your OpenAI API Key respectively

## How to use
Run the main.py file. Then, all you have to do is write a message into the channel that you set the bot to look for messages and the bot will reply. Just make sure that you set the channel and server id correctly. (Check configuration for more information )

# Configuration

### Setting Owner and Server ID

Check the link for more help [here](https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/)

### Changing the chatgpt model

If you want to change the chatgpt model, you can change the following line to be one of the other models listed [here](https://platform.openai.com/docs/models):
```model="model_name", #gpt-4.1-nano```
in openai_chat.py

### Changing how chatgpt acts

If you want to change the 'personality' of chatgpt, you can make or delete new roles in the roles.py file. Just make it the same layout as the sample roles.


