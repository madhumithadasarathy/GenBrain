import spacy

# Load spaCy's medium English model
nlp = spacy.load("en_core_web_sm")

def extract_tags(text, max_tags=5):
    """
    Extracts relevant tags (noun phrases, named entities) from the input text.

    Args:
        text (str): The input text to extract tags from.
        max_tags (int): Maximum number of tags to return.

    Returns:
        List[str]: A list of tags/keywords.
    """
    if len(text.strip()) == 0:
        return ["(No tags - empty input)"]

    doc = nlp(text)
    tags = set()

    # Add named entities (e.g. "OpenAI", "New York")
    for ent in doc.ents:
        tags.add(ent.text)

    # Add noun chunks (e.g. "generative AI", "training data")
    for chunk in doc.noun_chunks:
        tags.add(chunk.text)

    # Convert to list and limit
    return list(tags)[:max_tags]
