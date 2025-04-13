from flask import Flask, session
import threading
import subprocess
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session = Session(app)
# Your Flask route
@app.route('/')
def home():
    session['chat_id'] = '1234567890'  # Example chat ID
    return f"Chat ID is: , Numb is: "

# Function to run the external bot
def run_bot():
    chat_id = session.get('chat_id')
      # Clear session after getting chat_id
    subprocess.run(["python", "send1.py", chat_id, "55"])

if __name__ == '__main__':
    # Start the bot in a separate thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Start the Flask app
    app.run(debug=True, use_reloader=False)
