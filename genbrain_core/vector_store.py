import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "notes"

# Use the same model as in linker.py for consistency
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/all-mpnet-base-v2")

class VectorStore:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=sentence_transformer_ef
        )

    def add_note(self, note_id, text, metadata):
        self.collection.add(
            ids=[note_id],
            documents=[text],
            metadatas=[metadata]
        )

    def search_similar(self, query_text, n_results=3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "summary": results['metadatas'][0][i].get("summary", ""),
                    "score": round(1 - results['distances'][0][i], 2) # Chroma returns distance, we want similarity
                })
        return formatted_results

    def get_all_notes(self):
        results = self.collection.get()
        notes = []
        for i in range(len(results['ids'])):
            notes.append({
                "id": results['ids'][i],
                "text": results['documents'][i],
                "metadata": results['metadatas'][i]
            })
        return notes
