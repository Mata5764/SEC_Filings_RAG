import json
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JSON_PATH = "app/data/json/llama_parsed_exxon_10k.json"  # Path to your JSON file (located in the data folder)
CHROMA_DIR = "app/data/chroma_db"  # Path to Chroma DB directory


def load_json_to_documents(file_path):
    """
    Load JSON data and convert to LangChain Document objects with custom metadata.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    documents = []
    actual_page = 1
    for i, entry in enumerate(data):
        text_content = entry.get('text', '')
        if text_content == "NO_CONTENT_HERE" or not text_content.strip():
            continue
        metadata = {
            'source': 'exxon_10k',
            'page': actual_page,
            'original_index': i
        }
        doc = Document(
            page_content=text_content,
            metadata=metadata
        )
        documents.append(doc)
        actual_page += 1
    return documents

def get_or_create_document_store(documents, persist_directory=CHROMA_DIR):
    """
    Load the Chroma document store from disk if it exists, otherwise create and persist it.
    """
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        document_store = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        ))
        print("Loaded existing Chroma vector store from disk.")
    else:
        document_store = Chroma.from_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            ),
            persist_directory=persist_directory
        )
        document_store.persist()
        print("Created and persisted new Chroma vector store.")
    return document_store

def main():
    # Load documents from JSON
    docs = load_json_to_documents(JSON_PATH)
    print(f"Loaded {len(docs)} valid documents from {JSON_PATH}")
    # Create or load Chroma vector store
    get_or_create_document_store(docs, persist_directory=CHROMA_DIR)

if __name__ == "__main__":
    main() 