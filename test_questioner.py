from src.questioner import generate_questions

sample_text = """
Transformers are powerful models that rely on attention mechanisms to model relationships in text. 
They are used in tasks like summarization, translation, and question answering.
"""

questions = generate_questions(sample_text, num_return_sequences=3)

print("❓ Follow-Up Questions:\n")
for q in questions:
    print("•", q)
