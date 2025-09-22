from user_bot import *
from utils import *
import inspect

async def main():
    try:
        await client.start()
        print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
        asyncio.create_task(db_poller())
        asyncio.create_task(get_available_groups())
        await client.run_until_disconnected()
    except (telethon.errors.rpcerrorlist.TimeoutError, aiohttp.ClientError, ConnectionError) as e:
        print(f"Network error in main_bot at {inspect.currentframe().f_code.co_name}", e)
    except telethon.errors.FloodWaitError as e:
        print(f"Flood wait error in main_bot at {inspect.currentframe().f_code.co_name}", e)
    except telethon.errors.AuthKeyUnregisteredError as e:
        print(f"Session invalid in main_bot at {inspect.currentframe().f_code.co_name}", e)
    except asyncio.exceptions.CancelledError as e:
        print(f"Main bot cancelled {inspect.currentframe().f_code.co_name}", e)
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())