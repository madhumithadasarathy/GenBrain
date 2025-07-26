from genbrain_core.engine import process_note

# Sample input paragraph
sample_text = """
Generative AI is revolutionizing how we produce content. With tools like ChatGPT, DALL·E, and BART,
it's now possible to generate human-like text, images, and even code. These models are trained on
massive datasets and can perform tasks like summarization, translation, and creative writing. 
As they become more powerful, they are being integrated into everyday apps for productivity,
education, and creativity.
"""

# Run summarizer
summary = summarize_text(sample_text)

print("📝 Original Text:\n", sample_text)
print("\n🧠 AI Summary:\n", summary)
