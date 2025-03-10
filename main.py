from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is your LINE Bot!"

@app.route('/webhook', methods=['POST'])
def webhook():
    return "Webhook received!", 200  # ✅ ต้องคืนค่า 200

if __name__ == "__main__":
    app.run()
