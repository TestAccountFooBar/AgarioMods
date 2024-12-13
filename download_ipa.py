import os
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
APP_STORE_LINK = "https://apps.apple.com/app/id995999703"  # Agar.io
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_app_link():
    """Send the App Store link to EeveeDecrypterBot."""
    message = f"@eeveedecrypterbot {APP_STORE_LINK}"
    url = f"{TELEGRAM_API_BASE}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    logger.info("Sending App Store link to EeveeDecrypterBot...")
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logger.info("Message sent successfully.")
    else:
        logger.error(f"Failed to send message: {response.text}")


def fetch_latest_messages():
    """Fetch the latest messages sent to the bot."""
    url = f"{TELEGRAM_API_BASE}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        logger.error(f"Failed to fetch messages: {response.text}")
        return []


def download_file(file_id, file_name):
    """Download a file from Telegram."""
    # Get file path
    url = f"{TELEGRAM_API_BASE}/getFile"
    response = requests.get(url, params={"file_id": file_id})
    if response.status_code == 200:
        file_path = response.json()["result"]["file_path"]

        # Download the file
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        file_response = requests.get(file_url, stream=True)
        if file_response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in file_response.iter_content(chunk_size=1024):
                    file.write(chunk)
            logger.info(f"File downloaded successfully: {file_name}")
        else:
            logger.error(f"Failed to download file: {file_response.text}")
    else:
        logger.error(f"Failed to get file path: {response.text}")


def wait_for_file():
    """Poll for a file response from EeveeDecrypterBot."""
    logger.info("Waiting for decrypted IPA...")
    while True:
        messages = fetch_latest_messages()
        for message in messages:
            if "document" in message.get("message", {}):
                document = message["message"]["document"]
                file_id = document["file_id"]
                file_name = "Agario.ipa"
                download_file(file_id, file_name)
                return
        logger.info("Sleeping for five seconds...")
        time.sleep(5)  # Avoid spamming the API
        


if __name__ == "__main__":
    if not BOT_TOKEN:
        logger.error("Bot token not provided. Set TELEGRAM_BOT_TOKEN in environment.")
    else:
        send_app_link()
        wait_for_file()
