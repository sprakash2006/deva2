# main.py – Starts Telegram bot and background RAG watcher

from dotenv import load_dotenv
from deva_telegram_bot import DevaTelegramBot
from openai_agent import OpenAIAgent
from rag_retriever import RAGRetriever
from telegram.error import TelegramError
from telegram.ext import ContextTypes
import threading
import os

# Load environment variables
load_dotenv()

# Async error handler
def handle_error(update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    try:
        raise error
    except TelegramError as te:
        print(f"Telegram error occurred: {te}")
    except Exception as e:
        print(f"Unhandled error: {e}")

# Background RAG ingestion loop
from rag_watcher import watch_loop

# def start_rag_thread():
#     thread = threading.Thread(target=watch_loop, args=(60,), daemon=True)
#     thread.start()
#     print("📡 Background RAG watcher started.")

def main():
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not tg_token or not openai_key:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY in environment.")

    # Start RAG watcher in background
    # start_rag_thread()

    # Initialize AI and RAG agents
    ai_agent = OpenAIAgent(api_key=openai_key)
    rag_agent = RAGRetriever(api_key=openai_key)

    # Initialize bot
    bot = DevaTelegramBot(token=tg_token, ai_agent=ai_agent, rag_retriever=rag_agent)
    bot.application.add_error_handler(handle_error)

    # Start bot
    bot.run()

if __name__ == "__main__":
    main()
