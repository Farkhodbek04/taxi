import os
import telethon
import asyncio
import random
import aiohttp
from rapidfuzz import process, fuzz
from telethon.types import Channel

from db_manager import *
from config import *
from funcs import *
from utils import *

# Global variables to store configuration
source_id = {}
destination_id = {}
keywords = set()
negatives = set()
groups_cache = {}
sender_cache = {}
# Load initial configurations
def load_db():
    global source_id, destination_id, keywords, negatives, groups_cache
    try: 
        source_id = set(int(id1) for id1 in read_db('groups_dict').get('source_id', {}).keys())
        destination_id = set(int(id1) for id1 in read_db('groups_dict').get('destination_id', {}).keys())
        keywords = set(read_db('keywords')['keywords'])
        negatives = set(ng for ng in read_db('keywords').get('negatives', {}))
        groups_cache = read_db('groups_dict').get('groups_cache', {})
        # print(f"Source ids: {source_id}")
        # print(f"Destination: {destination_id}")
        # print(f"keywords: {keywords}")
        # print(f"negatives: {negatives}")
        # print(f"groups: {groups_cache}")
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)
# Initial load
try:
    load_db()
except Exception as e:
    print(f"Failed to load initial db: {str(e)}")
    raise


# filter client messages
async def is_client_request(message:str) -> bool:
    if message.startswith("👤"):
        return True
    
    
    keywords = set(read_db('keywords')['keywords'])
    negatives = set(ng for ng in read_db('keywords').get('negatives', {}))

        
    if sum(1 if val.lower() in negatives else 0 for val in message.split()) >= 1:
        return False
    
    words = message.split()
    if len(words) > 15:
        return False
    
    for word in words:
        if word.startswith("https"):
            return False
    
    if not words:
        return False
    if not keywords:  # Check if keywords is empty
        return False
    try:
        loop = asyncio.get_event_loop()
        matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
        total_words = len(words)
        match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
        if total_words <= 8:
            return match_percentage >= 55
        elif total_words >= 9:
            return match_percentage >= 60
    except Exception as e:
        error_msg = f"Error in is_client_request: {str(e)}"
        print(error_msg)
        # if bot and SUPERADMIN:
        #     await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        # return False

async def send_formatted_message(client, event, sender, dest_id, chat_id, message_text):
    # Build message link (only works for public groups/channels)
    if event.is_channel and isinstance(await event.get_chat(), Channel):
        chat = await event.get_chat()
        if hasattr(chat, 'username') and chat.username:
            message_link = f"https://t.me/{chat.username}/{event.id}"
        else:
            message_link = None
    else:
        message_link = None

    # Format message
    if sender is not None and not getattr(sender, "bot", False):
        username = getattr(sender, 'username', None)
        first_name = getattr(sender, 'first_name', 'Foydalanuvchi')
        user_display = f"@{username}" if username else first_name
        phone = getattr(sender, 'phone', None)
        formatted_message = (
            f"<b>Mijoz: </b> {user_display}\n"
            f"<b>Xabar: </b> {message_text}\n\n"
        )
        if phone:
            formatted_message += f"<b>Telefon: </b> +{phone}\n"
        if message_link:
            formatted_message += f"<b>Guruh: </b> <a href='{message_link}'> guruh</a>"
    else:
        formatted_message = (
            f"{message_text}\n"
        )
        if message_link:
            formatted_message += f"<b>Guruh: </b> <a href='{message_link}'> guruh</a>"

    for des in destination_id:
        entity = await client.get_entity(int(des))
        print(f"Sending to {des}")
        await client.send_message(
            entity=entity,
            message=formatted_message,
            parse_mode='html'
        )


async def db_poller():
    last_updated_groups = os.path.getmtime('db/groups_dict.json')
    last_updated_keywords = os.path.getmtime('db/keywords.json')
    try:
        while True:
            await asyncio.sleep(10)
            current_updated_groups = os.path.getmtime('db/groups_dict.json')
            current_updated_keywords = os.path.getmtime('db/keywords.json')
            if (current_updated_groups!=last_updated_groups) or (current_updated_keywords!=last_updated_keywords):
                load_db()
                last_updated_keywords = current_updated_keywords
                last_updated_groups = current_updated_groups
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)
        raise


