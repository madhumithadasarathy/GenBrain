from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_questions(summary, num_return_sequences=3):
    prompt = f"Generate {num_return_sequences} follow-up questions based on this summary:\n{summary}"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Split into individual questions (assumes line breaks or bullets)
    questions = [q.strip("• ").strip() for q in output.strip().split('\n') if q.strip()]
    
    return questions[:num_return_sequences]
