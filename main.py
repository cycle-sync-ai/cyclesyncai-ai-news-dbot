from telethon import TelegramClient, events
import discord
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Define folders for saving images and videos
IMAGE_FOLDER = "images"
VIDEO_FOLDER = "videos"
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Initialize the Telegram client
telegram_client = TelegramClient('session_name', API_ID, API_HASH)

# Initialize the Discord client with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.messages = True #enable message intents
discord_client = discord.Client(intents=intents)

# Use the channel username or ID (ensure it's correct)
channel_username = '@test1108123123'  # Use just the channel ID without 'https://web.telegram.org/k/#'

@telegram_client.on(events.NewMessage(chats=channel_username))
async def telegram_handler(event): #renamed handler to telegram_handler to avoid collision
    message_text = event.message.text or "No text in this message."

    if event.message.photo:
        print(f"🖼️ Image detected! Message: {message_text}")
        file_path = await event.message.download_media(file=IMAGE_FOLDER)
        print(f"✅ Image saved to: {file_path}")
        await send_photo_to_discord(file_path, message_text)

    elif event.message.video:
        print(f"🎥 Video detected! Message: {message_text}")
        file_path = await event.message.download_media(file=VIDEO_FOLDER)
        print(f"✅ Video saved to: {file_path}")
        await send_video_to_discord(file_path, message_text)

    else:
        print(f"💬 Text Message: {message_text}")
        await send_text_to_discord(message_text)

# Separate functions for sending different types of content to Discord
async def send_text_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

async def send_photo_to_discord(file_path, message_text):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        try:
            with open(file_path, 'rb') as fp:
                await channel.send(file=discord.File(fp, filename=os.path.basename(file_path)), content=message_text)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"Error sending photo to Discord: {e}")

async def send_video_to_discord(file_path, message_text):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        try:
            with open(file_path, 'rb') as fp:
                await channel.send(file=discord.File(fp, filename=os.path.basename(file_path)), content=message_text)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"Error sending video to Discord: {e}")

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')

async def main():
    async with telegram_client:
        await telegram_client.start() #start telegram client
        await discord_client.start(DISCORD_TOKEN)  # Start Discord client
        print("Message Scraping Start...")
        await telegram_client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
