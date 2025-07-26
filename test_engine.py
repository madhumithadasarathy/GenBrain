from src.engine import process_note

note = """
Large language models like ChatGPT are based on the transformer architecture. 
They are trained on diverse internet data and can perform various NLP tasks including summarization, translation, Q&A, and more.
"""

result = process_note(note)

print("\n🧠 Processed Note:")
print("Summary:", result["summary"])
print("Tags:", result["tags"])
print("Questions:")
for q in result["questions"]:
    print(" •", q)

print("\n🔗 Related Notes:")
for r in result["related_notes"]:
    print(f"→ Score: {r['score']:.2f} | Summary: {r['summary']}")
