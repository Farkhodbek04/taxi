import os
import json

import telethon
from telethon.types import Channel, Chat
from telethon.errors import FloodWaitError
import asyncio
import inspect

from config import *
from funcs import *
from db_manager import read_db
from utils import *

client = telethon.TelegramClient("my_client", int(API_ID), API_HASH) # type: ignore
# session lock
session_lock = asyncio.Lock()


@client.on(telethon.events.NewMessage(chats=source_id, incoming=True))
async def handler(event: telethon.events.newmessage.NewMessage.Event):
    try:
        dest_ids = list(read_db('groups_dict')['destination_id'].keys())
        chat_id = event.chat_id
        message_text = event.message.message
        sender_id = event.sender_id
        if str(sender_id).endswith("2227900964"):
            message_text.replace("👤", "")
            await client.send_message(
                    dest_ids[1],
                    message=message_text,
                    parse_mode='html'
                )
        if message_text.startswith("🚕 "):
            message_text.replace("🚕", "")
            await client.send_message(
                    dest_ids[1],
                    message=message_text,
                    parse_mode='html'
                )

        sender = sender_cache.get(sender_id)
        if sender is None:
            try:
                sender = await event.get_sender()
                if sender is not None:
                    sender_cache[sender_id] = sender
            except FloodWaitError as e:
                print(f"Flood wait: sleeping for {e.seconds} seconds (get_sender)")
                await asyncio.sleep(e.seconds)
                sender = None
            except Exception as e:
                print(f"Error at handler (get_sender): {e}")
                sender = None

        # ADD THIS CHECK: skip if sender is a bot
        if sender is not None and getattr(sender, "bot", False):
            return

        if await is_client_request(message_text):
            if dest_ids:
                des_id = dest_ids[0]
                try:
                    await send_formatted_message(client, event, sender, des_id, chat_id, message_text)
                except FloodWaitError as e:
                    print(f"Flood wait: skipping sending for {e.seconds} seconds")
                except Exception as e:
                    print(f"Error at handler {e}")
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)

async def get_available_groups():
    groups = await refresh_groups_cache(client)
    print("All groups extracted")
    with open('db/all_available_groups.json', 'w', encoding='utf-8') as file:
        json.dump(groups, file, indent=4, ensure_ascii=False)
    return True