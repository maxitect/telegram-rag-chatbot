import chromadb
import hashlib
from typing import List, Dict, Any
from pathlib import Path

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class ChromaModule:
    def __init__(
            self,
            persist_directory: str = "./chroma_db",
            collection_name: str = "documents"
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def chunk_text(
            self, text: str, chunk_size: int = 500
    ) -> List[str]:
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    words = paragraph.split()
                    for i in range(0, len(words), chunk_size // 10):
                        chunk = ' '.join(words[i:i + chunk_size // 10])
                        chunks.append(chunk)
            else:
                current_chunk += (
                    "\n\n" + paragraph if current_chunk else paragraph
                )

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def generate_chunk_id(self, file_path: str, chunk_index: int) -> str:
        content = f"{file_path}_{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()

    def ingest_documents(self, docs_folder: str = "./docs"):
        docs_path = Path(docs_folder)

        if not docs_path.exists():
            raise FileNotFoundError(f"Directory {docs_folder} does not exist")

        batch_size = 50
        batch_documents = []
        batch_metadatas = []
        batch_ids = []

        for file_path in docs_path.rglob("*.md"):
            print(f"Processing: {file_path}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                chunks = self.chunk_text(content)

                for i, chunk in enumerate(chunks):
                    chunk_id = self.generate_chunk_id(str(file_path), i)

                    existing = self.collection.get(ids=[chunk_id])
                    if existing['ids']:
                        continue

                    metadata = {
                        "source": str(file_path.relative_to(docs_path)),
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "file_type": "markdown"
                    }

                    batch_documents.append(chunk)
                    batch_metadatas.append(metadata)
                    batch_ids.append(chunk_id)

                    if len(batch_documents) >= batch_size:
                        self.collection.add(
                            documents=batch_documents,
                            metadatas=batch_metadatas,
                            ids=batch_ids
                        )
                        batch_documents = []
                        batch_metadatas = []
                        batch_ids = []
                        print(f"Added batch of {batch_size} chunks")

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

        if batch_documents:
            self.collection.add(
                documents=batch_documents,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            print(f"Added final batch of {len(batch_documents)} chunks")

    def query_documents(
            self, query: str, n_results: int = 5
    ) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': (
                    results['distances'][0][i]
                    if 'distances' in results else None
                )
            })

        return formatted_results
