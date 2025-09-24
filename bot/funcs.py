import inspect

import telethon
from telethon.types import Channel, Chat

async def refresh_groups_cache(client: telethon.TelegramClient):
    
    groups_cache = {}
    try:
        await client.start()
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            # Include meagagroups and normal groups
            if isinstance(entity, Channel) and entity.megagroup:
                group_id = entity.id
                name = entity.title
                id_str = f"-100{str(group_id)}"
                if entity.username:
                    link = f"https://t.me/{entity.username}"
                    groups_cache[id_str] = f"[{name}]({link})"
                else:
                    groups_cache[id_str] = f"{name}"
            elif isinstance(entity, Chat):
                group_id = entity.id
                name = entity.title
                id_str = f"-{str(group_id)}"
                groups_cache[id_str] = f"[{name}]({link})"
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)
        raise
    return groups_cache

