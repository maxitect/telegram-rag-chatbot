from chroma_module import ChromaModule

if __name__ == "__main__":
    chroma = ChromaModule()
    print("Starting document ingestion...")
    chroma.ingest_documents("./docs")
    print("Document ingestion completed.")

    count = chroma.collection.count()
    print(f"Total chunks in database: {count}")
