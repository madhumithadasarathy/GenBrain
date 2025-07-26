from transformers import pipeline

# Load a text-to-text generation model
question_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base"
)

def generate_questions(text, num_return_sequences=3):
    """
    Generates questions based on the input note text.
    """
    if len(text.strip()) == 0:
        return ["(No questions - input is empty)"]

    prompt = f"Generate {num_return_sequences} questions from this:\n{text}"

    results = question_generator(
        prompt,
        max_length=100,
        do_sample=True,
        top_k=50,
        num_return_sequences=num_return_sequences
    )

    return [r['generated_text'] for r in results]
