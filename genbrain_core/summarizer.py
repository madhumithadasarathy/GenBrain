from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/pegasus-xsum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def chunk_text(text, max_tokens=512):
    """Split text into manageable chunks for the model."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)

def summarize_chunk(text, max_length=64):
    """Summarize a single chunk of text."""
    inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_text(text, max_length=150):
    """
    Summarizes the input text. For large documents, it uses a recursive chunking strategy.
    """
    # If the text is short, summarize directly
    tokens = tokenizer.encode(text)
    if len(tokens) <= 512:
        return summarize_chunk(text, max_length=max_length)
    
    # Otherwise, summarize in chunks
    print(f"Document is large ({len(tokens)} tokens). Using recursive summarization...")
    chunks = list(chunk_text(text))
    chunk_summaries = [summarize_chunk(c, max_length=64) for c in chunks]
    
    # Combine chunk summaries and summarize again
    combined_summary_text = " ".join(chunk_summaries)
    
    # Final pass
    return summarize_chunk(combined_summary_text, max_length=max_length)
