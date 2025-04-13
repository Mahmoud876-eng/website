import threading
import subprocess
numb="55"
id="1234567890"
# Function to run the bot (separate process)
def run_bot():
    subprocess.run(["python", "send1.py",numb,id])

# Function to run the Flask app (separate process)
def run_flask():
    subprocess.run(["python", "app.py"])

# Start both bot and Flask in separate threads
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_flask).start()
