import json
import os
from datetime import datetime

from genbrain_core.summarizer import summarize_text
from genbrain_core.tagger import extract_tags
from genbrain_core.questioner import generate_questions
from genbrain_core.vector_store import VectorStore

NOTES_PATH = "data/notes.json"
vector_store = VectorStore()

def migrate_json_to_chroma():
    if not os.path.exists(NOTES_PATH):
        return
    
    with open(NOTES_PATH, "r", encoding="utf-8") as f:
        notes = json.load(f)
    
    print(f"Migrating {len(notes)} notes to ChromaDB...")
    for i, note in enumerate(notes):
        note_id = f"note_{i}_{datetime.now().timestamp()}"
        vector_store.add_note(
            note_id=note_id,
            text=note["text"],
            metadata={
                "timestamp": note.get("timestamp", datetime.now().isoformat()),
                "summary": note["summary"],
                "tags": ",".join(note.get("tags", [])),
            }
        )
    # Rename old file to avoid re-migration
    os.rename(NOTES_PATH, NOTES_PATH + ".bak")
    print("Migration complete.")

def load_notes():
    # Return notes from ChromaDB in the format the UI expects
    results = vector_store.get_all_notes()
    formatted = []
    for item in results:
        formatted.append({
            "timestamp": item["metadata"].get("timestamp"),
            "text": item["text"],
            "summary": item["metadata"].get("summary"),
            "tags": item["metadata"].get("tags", "").split(",") if item["metadata"].get("tags") else [],
            "questions": [], # Questions aren't stored in metadata for now to keep it simple
            "related_notes": []
        })
    return formatted

def process_note(raw_text):
    print("Processing Note...")

    summary = summarize_text(raw_text)
    tags = extract_tags(raw_text)
    questions = generate_questions(raw_text, num_return_sequences=3)
    
    # Use ChromaDB for similar notes
    links = vector_store.search_similar(raw_text, n_results=3)

    note_id = f"note_{datetime.now().timestamp()}"
    note_metadata = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary.strip(),
        "tags": ",".join(tags),
    }

    # Save to ChromaDB
    vector_store.add_note(note_id, raw_text.strip(), note_metadata)

    return {
        "timestamp": note_metadata["timestamp"],
        "text": raw_text.strip(),
        "summary": summary.strip(),
        "tags": tags,
        "questions": questions,
        "related_notes": links
    }

# Run migration on import
migrate_json_to_chroma()
