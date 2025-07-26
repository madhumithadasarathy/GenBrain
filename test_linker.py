from src.linker import get_similar_notes

new_note = """
Transformer-based models are incredibly powerful for processing language.
They use attention mechanisms to capture contextual relationships between words.
"""

results = get_similar_notes(new_note, top_k=2)

print("🔗 Top Similar Notes:\n")
for res in results:
    print(f"→ Score: {res['score']:.2f}")
    print(f"Summary: {res['summary']}")
    print(f"Text: {res['text']}\n")
