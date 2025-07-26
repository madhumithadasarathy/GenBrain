from genbrain_core.tagger import extract_tags

sample_text = """
Generative AI like ChatGPT and BERT are trained on huge datasets. These models are changing how content is written in companies like Google and Microsoft.
"""

tags = extract_tags(sample_text)

print("Extracted Tags:", tags)
