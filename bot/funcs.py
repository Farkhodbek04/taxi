import inspect

import telethon
from telethon.types import Channel, Chat
import json
import inspect
from telethon import functions, types

# Helper to build a clickable label (name + link if available)
def _label(name: str, username: str | None) -> str:
    if username:
        return f"[{name}](https://t.me/{username})"
    return name

async def refresh_groups_cache(client):
    groups_cache: dict[str, str] = {}
    try:
        # Ensure you're already authorized/started BEFORE calling this function.
        # await client.start()  # <- Prefer starting the client outside.

        # 1) Discover available dialog folders (All=0, Archived=1, plus custom)
        folders = [0, 1]  # All, Archived
        try:
            filters = await client(functions.messages.GetDialogFiltersRequest())
            # Custom folders have IDs starting from 2
            # (each filter has .id, .title; we only need .id)
            for f in filters:
                if getattr(f, 'id', None) not in (None, 0, 1):
                    folders.append(f.id)
        except Exception:
            # Older Telegram versions/accounts might not support filters – ignore
            pass

        seen = set()  # avoid duplicates across folders

        for folder_id in folders:
            async for dialog in client.iter_dialogs(folder=folder_id, limit=None):
                entity = dialog.entity
                # Supergroups (Channel with megagroup=True)
                if isinstance(entity, types.Channel) and entity.megagroup:
                    tg_id = f"-100{entity.id}"          # chat_id form for supergroups
                    if tg_id in seen:
                        continue
                    seen.add(tg_id)
                    groups_cache[tg_id] = _label(entity.title, entity.username)

                # Basic groups (types.Chat)
                elif isinstance(entity, types.Chat):
                    tg_id = f"-{entity.id}"             # chat_id form for basic groups
                    if tg_id in seen:
                        continue
                    seen.add(tg_id)
                    # Basic groups don’t have public usernames; just store the title
                    groups_cache[tg_id] = entity.title

                # OPTIONAL: include broadcast channels too (if you want *all* channels)
                # elif isinstance(entity, types.Channel) and not entity.megagroup:
                #     # Broadcast channel (not a group), include if desired:
                #     tg_id = f"-100{entity.id}"
                #     if tg_id in seen:
                #         continue
                #     seen.add(tg_id)
                #     groups_cache[tg_id] = _label(entity.title, entity.username)

    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}: {e}")
        raise

    return groups_cache
