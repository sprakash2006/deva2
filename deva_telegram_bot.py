# Final deva_telegram_bot.py with asyncio.run fix for run_polling()

import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

from openai_agent import OpenAIAgent
from rag_retriever import RAGRetriever
from message_analyzer import MessageAnalyzer
from persistent_memory import PersistentMemory
from translation import translate_to_english, translate_from_english

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DevaTelegramBot:
    def __init__(self, token, ai_agent, rag_retriever):
        self.token = token
        self.ai_agent = ai_agent
        self.rag_retriever = rag_retriever

        self.analyzer = MessageAnalyzer()
        self.memory = PersistentMemory()

        self.application = ApplicationBuilder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            await update.message.reply_text(
                "Hi, I’m DEVA 🌟\nI can help based on institutional documents already available. Just ask!"
            )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return

        try:
            user_id = str(update.message.from_user.id)
            user_input = update.message.text

            lang = self.analyzer.detect_language(user_input)
            logger.info(f"Detected language: {lang}")

            query_english = translate_to_english(user_input, lang)
            tone = self.analyzer.analyze_sentiment(user_input)
            logger.info(f"Detected sentiment tone: {tone}")

            memory = self.memory.get(user_id)

            rag_answer = self.rag_retriever.query(query_english)
            final_english = rag_answer

            final_reply = translate_from_english(final_english, lang)

            self.memory.append(user_id, "user", user_input)
            self.memory.append(user_id, "assistant", final_reply)

            await update.message.reply_text(final_reply[:4096])

        except Exception as e:
            logger.error(f"Error in multilingual handle_text: {e}", exc_info=True)
            await update.message.reply_text("⚠️ Error processing your request. Please try again.")

    def run(self):
        logger.info("🤖 DEVA Bot running with RAG-only mode...")
        asyncio.run(self.application.run_polling())
