import stanza

# Load Stanza pipeline (this will download the English model if not already available)
stanza_nlp = stanza.Pipeline('en')

# Now use stanza_nlp as a spaCy-like pipeline
text = "She gave her book to the librarian, and she walked away."

# Process the text
doc = stanza_nlp(text)

# You can now use spaCy-like syntax to interact with the document
print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')

print(doc.sentences)
