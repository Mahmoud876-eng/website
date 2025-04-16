from telegram import Bot
from apscheduler.schedulers.background import AsyncIOScheduler ,  BackgroundScheduler
import datetime
import time
import asyncio
import variable

# Replace with your bot token and the chat ID of the person
BOT_TOKEN = variable.TOKEN  # Replace with your actual bot token
CHAT_ID= variable.CHAT_ID  # Replace with your actual chat ID

async def send_message():
    await bot.send_message(chat_id=CHAT_ID, text="⏰ Hey! It's time to take your medicine!")

bot = Bot(token=BOT_TOKEN)
def schedule_send_message():
    asyncio.run(send_message())

# Create a scheduler
#scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()
scheduler.add_job(schedule_send_message, 'cron', minute='*')

scheduler.start()
# Schedule the message (example: at 10:30 AM every day)
print("Scheduler started. Waiting to send messages...")
try:
    while True:
        time.sleep(1)
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")