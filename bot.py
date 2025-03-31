import discord
import openai
import os

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.threads = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[READY] Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot or not isinstance(message.channel, discord.Thread):
        return

    if client.user in message.mentions:
        await message.channel.typing()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant in a Discord thread."},
                {"role": "user", "content": message.content}
            ]
        )
        await message.reply(response['choices'][0]['message']['content'])

client.run(DISCORD_TOKEN)