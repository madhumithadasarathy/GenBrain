from transformers import pipeline

# Load the upgraded FLAN-T5 base model
question_generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_questions(summary, num_return_sequences=3):
    prompt = f"Generate {max_questions} follow-up questions based on this summary:\n{summary}"
    
    result = question_generator(prompt, max_length=100, num_return_sequences=1, clean_up_tokenization_spaces=True)
    
    output = result[0]['generated_text']

    # Split into individual questions (assumes line breaks or bullets)
    questions = [q.strip("• ").strip() for q in output.strip().split('\n') if q.strip()]
    
    return questions[:num_return_sequences]
