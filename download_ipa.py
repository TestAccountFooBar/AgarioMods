import os
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

APP_STORE_LINK = "https://apps.apple.com/app/id995999703"  # Agar.io


async def send_app_link(bot: Bot):
    """Send the App Store link to EeveeDecrypterBot."""
    eevee_bot_username = "@eeveedecrypterbot"
    logger.info("Sending App Store link to EeveeDecrypterBot...")
    try:
        message = await bot.send_message(chat_id=7106204388, text=f"{eevee_bot_username} {APP_STORE_LINK}") # personal chat
        logger.info(f"Message sent to EeveeDecrypterBot: {message.message_id}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise


async def fetch_decrypted_ipa(update: Update, context: CallbackContext):
    """Fetch the decrypted IPA file sent by EeveeDecrypterBot."""
    if update.message:
        file =await context.bot.get_file(update.message.document)
        file_name = "Agario.ipa"
        await file.download_to_drive(file_name)
        logger.info(f"File downloaded: {file_name}")


async def main():
    """Main function to handle messaging and file retrieval."""
    bot = Bot(BOT_TOKEN)
    if not BOT_TOKEN:
        logger.error("Bot token not provided. Set TELEGRAM_BOT_TOKEN in environment.")
        return
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.ATTACHMENT, fetch_decrypted_ipa))

    # Start the bot and send the app link
    polling_task = asyncio.create_task(application.run_polling())
    await send_app_link(bot)

    logger.info("Waiting for decrypted IPA...")

    await polling_task



if __name__ == "__main__":
    asyncio.run(main())