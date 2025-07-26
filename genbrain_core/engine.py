import json
import os
from datetime import datetime

from genbrain_core.summarizer import summarize_text
from genbrain_core.tagger import extract_tags
from genbrain_core.linker import get_similar_notes
from genbrain_core.questioner import generate_questions


NOTES_PATH = "data/notes.json"

def load_notes():
    if not os.path.exists(NOTES_PATH):
        return []
    with open(NOTES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_PATH, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

def process_note(raw_text):
    print("⚙️ Processing Note...")

    summary = summarize_text(raw_text)
    tags = extract_tags(raw_text)
    links = get_similar_notes(raw_text, top_k=3)
    questions = generate_questions(raw_text, num_return_sequences=3)

    note = {
        "timestamp": datetime.now().isoformat(),
        "text": raw_text.strip(),
        "summary": summary.strip(),
        "tags": tags,
        "questions": questions,
        "related_notes": links
    }

    notes = load_notes()
    notes.append(note)
    save_notes(notes)

    return note
