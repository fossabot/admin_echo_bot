import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook

# Configure logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN'))
HEROKU_APP_NAME = os.getenv('APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    if message.chat.id == ADMIN and message.reply_to_message:
        await bot.send_message(chat_id=message.reply_to_message.forward_from.id, text=message.text)
    else:
        await message.reply('Запрос отправлен.')
        await bot.forward_message(chat_id=ADMIN, from_chat_id=message.chat.id, message_id=message.message_id)


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
