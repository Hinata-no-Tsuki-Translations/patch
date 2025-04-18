import spacy
import stanza

# Load spaCy English model
spacy_nlp = spacy.load("en_core_web_sm")

# Initialize Stanza (only once)
stanza.download('en')
stanza_pipeline = stanza.Pipeline(lang='en', processors='tokenize,pos')

# Pronoun replacement map
REPLACEMENTS = {
    "her": {"PRP": "him", "PRP$": "his"},
    "hers": "his",
    "herself": "himself",
    "she": "he"
}

def get_stanza_pos(text: str) -> dict:
    """Returns a dict mapping word text to its XPOS in Stanza."""
    doc = stanza_pipeline(text)
    word_tags = {}
    for sent in doc.sentences:
        for word in sent.words:
            word_tags[word.text] = word.xpos  # Use XPOS for finer tags
    return word_tags

def resolve_conflict(word: str, spacy_pos: str, stanza_pos: str) -> str:
    print(f"Conflict for word '{word}':")
    print(f"  spaCy POS: {spacy_pos}")
    print(f"  Stanza XPOS: {stanza_pos}")
    choice = input(f"Use which POS for '{word}'? (1 = spaCy [{spacy_pos}], 2 = Stanza [{stanza_pos}]): ").strip()
    if choice == '2':
        return stanza_pos
    return spacy_pos  # default to spaCy

def gender_flip(text: str) -> str:
    spacy_doc = spacy_nlp(text)
    stanza_pos_map = {}  # Lazy load only if needed
    out_tokens = []

    for token in spacy_doc:
        word = token.text
        lowered = word.lower()

        if lowered in REPLACEMENTS:
            rep = REPLACEMENTS[lowered]

            # If replacement depends on POS
            if isinstance(rep, dict):
                spacy_pos = token.tag_  # Use fine-grained tag like PRP vs PRP$
                
                # Lazily load Stanza only when needed
                if not stanza_pos_map:
                    stanza_pos_map = get_stanza_pos(text)
                stanza_pos = stanza_pos_map.get(word, spacy_pos)

                # Conflict resolution
                final_pos = spacy_pos
                if spacy_pos != stanza_pos:
                    final_pos = resolve_conflict(word, spacy_pos, stanza_pos)

                out = rep.get(final_pos, word)
            else:
                out = rep
        else:
            out = word

        # Preserve casing
        if word.istitle():
            out = out.capitalize()
        elif word.isupper():
            out = out.upper()

        out_tokens.append(out)

    return " ".join(out_tokens)

# Example usage
if __name__ == "__main__":
    input_text = "She gave her book to him because it was hers, and she helped herself."
    result = gender_flip(input_text)
    print("\nFinal Result:")
    print(result)
