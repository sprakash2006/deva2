# rag_watcher.py – Watches doc/rag_input/ and processes files for RAG

import os
import time
import shutil
import logging
from rag_ingestor import FileIngestor
from rag_retriever import RAGRetriever
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_watcher")

# New unified directory structure
BASE_DIR = "doc"
INPUT_DIR = os.path.join(BASE_DIR, "rag_input")
RAG_BEFORE = os.path.join(BASE_DIR, "rag_before")
RAG_DONE = os.path.join(BASE_DIR, "rag_done")
ALLOWED_EXT = {".pdf", ".txt", ".csv"}

# Create directories if missing
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(RAG_BEFORE, exist_ok=True)
os.makedirs(RAG_DONE, exist_ok=True)

def move_file(src_path, dest_folder):
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_folder, filename)
    shutil.move(src_path, dest_path)
    return dest_path

def process_file(filepath, rag: RAGRetriever):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in ALLOWED_EXT:
        logger.info(f"Skipping unsupported file: {filepath}")
        return

    moved_path = move_file(filepath, RAG_BEFORE)
    logger.info(f"Moved to processing: {moved_path}")

    ingestor = FileIngestor()
    chunks = ingestor.process_file(moved_path)

    if chunks:
        rag.add_documents(user_id="global", filename=os.path.basename(moved_path), chunks=chunks)
        logger.info(f"✅ Ingested {len(chunks)} chunks from {moved_path}")
        move_file(moved_path, RAG_DONE)
    else:
        logger.warning(f"❌ No content extracted from {moved_path}. Skipping.")

def watch_loop(interval=60):
    logger.info("📂 Watching doc/rag_input/ for new files...")
    rag = RAGRetriever(api_key=os.getenv("OPENAI_API_KEY"))

    while True:
        files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
        for fname in files:
            try:
                process_file(os.path.join(INPUT_DIR, fname), rag)
            except Exception as e:
                logger.error(f"Error processing {fname}: {e}", exc_info=True)
        time.sleep(interval)

if __name__ == "__main__":
    watch_loop()
