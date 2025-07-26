from transformers import pipeline

# Use PEGASUS model instead of BART for improved summarization
summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_text(text, max_length=100):
    """
    Summarizes the input text using the PEGASUS summarizer.

    Args:
        text (str): The input text to summarize.
        max_length (int): Maximum number of tokens in the summary.

    Returns:
        str: The generated summary.
    """
    result = summarizer(text, max_length=max_length, clean_up_tokenization_spaces=True)
    return result[0]["summary_text"]
