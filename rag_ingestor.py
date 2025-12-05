# rag_ingestor.py
import os
import fitz  # PyMuPDF
import docx

class FileIngestor:
    def process_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".pdf":
            text = self._extract_text_from_pdf(file_path)
        elif ext == ".txt":
            text = self._extract_text_from_txt(file_path)
        elif ext == ".docx":
            text = self._extract_text_from_docx(file_path)
        else:
            print(f"[WARN] Unsupported file type: {ext}")
            return 0

        chunks = self._split_into_chunks(text)
        print(f"[INFO] Extracted {len(chunks)} chunks from {file_path}")
        return chunks


    def _extract_text_from_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            print(f"[ERROR] PDF extraction failed: {e}")
            return ""

    def _extract_text_from_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def _extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _split_into_chunks(self, text, max_length=1000):
        paragraphs = text.split("\n\n")
        chunks, current_chunk = [], ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < max_length:
                current_chunk += para + "\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
