from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, SUPERADMIN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_error_to_admin(error_text: str):
    try:
        await bot.send_message(chat_id=SUPERADMIN, text=error_text, parse_mode="HTML")
        print("Error sent")
    except Exception as e:
        print(f"Failed to send error via aiogram: {e}")