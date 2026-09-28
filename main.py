import os
import threading
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from telegram import (
    Bot
)
from telegram.ext import (
    Updater
)
from telegram.error import TelegramError

ID = os.getenv("ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
DEBUG_USER_ID = os.getenv("DEBUG_USER_ID")
ADMIN = os.getenv("ADMIN").split()
API = os.getenv("API")

ASK_POST, ASK_TITLE, ASK_DESCRIPTION, ASK_PHOTO = range(4)


app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
CORS(app, resources={r"/*": {"origins": "https://249-school.uz"}})



@app.route("/")
def home():
    return "Use /get/<collection_id> to get collection data. For example: /get/1"

@app.route("/get/<int:collection_id>")
def get_message(collection_id):
    try:
        response = requests.get(
            f"https://api.smashdb.uz/get/{API}?type=collection&value={collection_id}",
            headers={"Content-Type": "application/json"},
        )
        return jsonify(response.json())

    except TelegramError as e:
        return jsonify({"error": e.message}), 400


def run_telegram_bot():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
