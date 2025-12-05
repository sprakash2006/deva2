# DEVA: Document-Enhanced Virtual Agent (Telegram + RAG)

DEVA is a multilingual, empathetic AI chatbot built for Telegram that uses a RAG (Retrieval-Augmented Generation) architecture to answer questions based on institutional documents.

---

## 🚀 Features

- 🤖 Telegram chatbot interface using OpenAI GPT.
- 📁 RAG pipeline using SentenceTransformer + ChromaDB.
- 🌐 Multilingual input + output with sentiment tone.
- 📂 Document ingestion via `doc/rag_input` folder (no file upload via bot).
- 🧠 User chat memory stored locally in SQLite.
- 🔁 Background RAG ingestion watcher.

---

## 🗂️ Folder Structure

```
deva/
├── doc/
│   ├── rag_input/      # Drop .pdf, .txt, .csv files here
│   ├── rag_before/     # Temp storage before RAG
│   └── rag_done/       # Processed documents
├── main.py             # Starts bot + watcher
├── deva_telegram_bot.py
├── rag_watcher.py
├── rag_retriever.py
├── rag_ingestor.py
├── openai_agent.py
├── message_analyzer.py
├── persistent_memory.py
├── translation.py
├── requirements.txt    # (You can generate using pip freeze)
```

---

## 🛠️ Setup

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Create `.env` file**

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

3. **Run the bot + watcher**

```bash
python main.py
```

---

## 💬 Usage

- Ask questions directly via Telegram.
- DEVA will respond **only from documents** in `doc/rag_input`.
- File upload via Telegram is **disabled**.

---

## 🧠 Memory

Chat history is stored in `chat_memory.db` and is used to retain conversational context per user.

---

## 🔄 Document Ingestion

Every 60 seconds:
- Files in `doc/rag_input/` are moved to `rag_before/`, processed, then archived in `rag_done/`.
- Supported: `.pdf`, `.txt`, `.csv`

---

## 📌 Notes

- Uses `SentenceTransformer(all-MiniLM-L6-v2)` for embedding.
- Uses `ChromaDB` as the vector store.

---

Step 1:
python .\rag_watcher.py

Step 2:
python .\main.py

