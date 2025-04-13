from flask import Flask, render_template , request
from telegram import Bot
import asyncio
import random
import variable
app=Flask(__name__)
TOKEN = variable.TOKEN
CHAT_ID = variable.CHAT_ID

    
@app.after_request
def print_status_code(response):
    print("Status code:", response.status_code)
    
    return response
async def send_message(message):
    bot=Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("yeah")
  
async  def get_messages():
        bot = Bot(token=TOKEN)
        print("getting messages")
        updates = await bot.get_updates()
        messages = [update.message.text for update in updates if update.message]
        if not updates:
            print("No new updates")
            return {"messages": []}
    
        return {"messages": messages}
    
@app.route("/register",  methods=["POST","GET"] )
def send():
    if request.method == "POST":
        
        
        
           
        # return "Message sent!"

        #asyncio.run(send_message("message"))
        number = random.randint(100, 1000)
        asyncio.run(send_message(f"your code is {number}"))

        return render_template("pop_up.html", number=number,message="open your telegram and type:")
    return render_template("register.html")
@app.route("/home", methods=["POST","GET"] )
def home():
    if request.method == "POST":
        cc=asyncio.run(get_messages())
        
        print(cc)
        if not cc:
            return render_template("register.html")
    return render_template("index.html")
    
if __name__ == '__main__':
    #debug=True # Enable debug mode
    #app.run()
    app.run(debug=True)
    