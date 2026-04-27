from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/pegasus-xsum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text, max_length=100):
    """
    Summarizes the input text using the PEGASUS model directly.
    """
    inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    
    # Generate summary
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, num_beams=4, length_penalty=2.0, early_stopping=True)
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
