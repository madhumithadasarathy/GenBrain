from genbrain_core.questioner import generate_questions

summary = "Transformers are deep learning models that use self-attention. They are commonly used in NLP tasks like summarization and translation."

questions = generate_questions(summary)

print("❓ Follow-Up Questions:\n")
for q in questions:
    print(f"• {q}")
