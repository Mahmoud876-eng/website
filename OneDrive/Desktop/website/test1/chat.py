from flask import Flask, session, request, render_template
import threading
import subprocess
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session = Session(app)
#chat_id = None  # Initialize chat_id globally

# Your Flask route
@app.route('/register', methods=["POST", "GET"])
def home():
    if request.method == "POST":
  # Example chat ID
        # Get chat_id from session
        chat_id = '1234567890'
        threading.Thread(target=run_bot, args=(chat_id,), daemon=True).start()  # Pass chat_id to run_bot
        return f"Chat ID is: {chat_id}, Numb is: 55"
    return render_template("register.html")
# Function to run the external bot
def run_bot(chat_id):
    
    print(f"Running bot with chat_id: {chat_id}")
    subprocess.run(["python", "send1.py", chat_id, "55"])

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, use_reloader=False)
    