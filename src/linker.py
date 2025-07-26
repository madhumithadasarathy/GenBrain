from sentence_transformers import SentenceTransformer, util
import json
import os

# Load the embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def load_existing_notes(path='data/notes.json'):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_similar_notes(new_text, top_k=3):
    """
    Finds the most semantically similar notes to the new_text.
    """
    notes = load_existing_notes()
    if not notes:
        return []

    # Get embeddings
    new_embedding = embedder.encode(new_text, convert_to_tensor=True)
    existing_texts = [note['text'] for note in notes]
    existing_embeddings = embedder.encode(existing_texts, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(new_embedding, existing_embeddings)[0]
    top_results = similarities.topk(top_k)

    similar_notes = []
    for score, idx in zip(top_results.values, top_results.indices):
        note = notes[int(idx)]
        similar_notes.append({
            'text': note['text'],
            'summary': note.get('summary', ''),
            'score': float(score)
        })

    return similar_notes
