from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is your LINE Bot!"

if __name__ == "__main__":
    app.run()
