from sentence_transformers import SentenceTransformer, util
import os
import json

# Load a more accurate model for better semantic similarity
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Sample notes database path
NOTES_PATH = "data/notes.json"

def get_similar_notes(new_note, top_k=3):
    # Load existing notes
    if os.path.exists(NOTES_PATH):
        with open(NOTES_PATH, "r") as f:
            notes = json.load(f)
    else:
        return []

    if not notes:
        return []

    # Extract text content
    existing_texts = [note["text"] for note in notes]

    # Compute embeddings
    new_embedding = model.encode(new_note, convert_to_tensor=True)
    existing_embeddings = model.encode(existing_texts, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(new_embedding, existing_embeddings)[0]

    # Get top-k similar notes
    top_results = sorted(
        zip(range(len(similarities)), similarities),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    results = []
    for idx, score in top_results:
        results.append({
            "text": notes[idx]["text"],
            "summary": notes[idx]["summary"],
            "score": round(float(score), 2)
        })

    return results
