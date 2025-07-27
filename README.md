# ChatGPT Discord Bot
This is a Discord bot (or app) that uses openai to give answers to questions with a command.

# The Setup
### Installing required packages
Copy "main.py" and "requirements.txt" into the same directory. Then open up a console and install the necessary packages using 
```pip install -r requirements.txt ```
or any other package manager

## Setting up API Key and Discord Token

If you do not have or know where to find the OpenAI API Key, there is a tutorial for that [here](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327).
Same with the Discord Token, [here](https://discordpy.readthedocs.io/en/stable/discord.html) (Make sure that the bot gets the "send messages" permission or just Admin if you're lazy like me)

Otherwise, you have two choices when setting up your API Keys

### API Keys using System environment variables

If you want to use System environment variables, you can delete line 9,  11 and 12 in main.py and change the line with the client variable to not have any api key in the OpenAI class.
Then, you will have to setup two system environment variables: DISCORD_TOKEN and OPENAI_API_KEY. If you don't know how to set up environment variables, you can see a tutorial [here](https://pureinfotech.com/create-custom-environment-variables-windows-10/). The values of the Token and Key should each be the token and the key that you got from discord and openai.

### API Keys using .env files

First, make a .env file in the directory with the main.py file. In this file you should write the following text:
```
DISCORD_TOKEN=your_token
OPENAI_API_KEY=your_api_key
```
where you should replace "your_token" and "your_api_key" with your Discord Token and your OpenAI API Key respectively

Now you can start the python file and test it out!

# How to use
blah blah blah blah
