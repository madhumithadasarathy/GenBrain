from transformers import pipeline

# Load a powerful summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=150, min_length=40):
    """
    Summarizes input text using BART with optional length constraints.
    """
    if len(text.strip()) == 0:
        return "⚠️ Input text is empty."

    # If input is too long, we'll chunk it in a later version
    result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return result[0]['summary_text']
