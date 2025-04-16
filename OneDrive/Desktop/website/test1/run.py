import threading
import subprocess
# Function to run the bot (separate process)
def run_bot():
    subprocess.run(["python", "send1.py"])
def run_send():
    subprocess.run(["python", "notifications.py"])

# Function to run the Flask app (separate process)
def run_flask():
    subprocess.run(["python", "app.py"])

# Start both bot and Flask in separate threads
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_send).start()
