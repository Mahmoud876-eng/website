from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Replace with your bot token and chat ID
BOT_TOKEN = "your_bot_token_here"  # Replace with your actual bot token
CHAT_ID = "your_chat_id_here"  # Replace with your actual chat ID

# Function to send a notification message
def send_notification():
    try:
        bot = Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text="⏰ Hey! This is your scheduled notification!")
        print("Notification sent successfully!")
    except Exception as e:
        print(f"Error sending notification: {e}")

# Create a scheduler
scheduler = BackgroundScheduler()

# Schedule the notification (example: every day at 10:30 AM)
scheduler.add_job(send_notification, 'cron', hour=10, minute=30)

# Start the scheduler
scheduler.start()

# Keep the script running
print("Scheduler started. Waiting to send notifications...")
try:
    while True:
        time.sleep(1)  # Keep the script running
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")