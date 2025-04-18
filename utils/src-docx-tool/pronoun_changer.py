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

def resolve_conflict(word: str, spacy_pos: str, stanza_pos: str, sentence_tokens: list, index: int) -> str:
    full_sentence = ' '.join(sentence_tokens)
    pointer_line = ' '.join(['^' if i == index else ' ' * len(tok) for i, tok in enumerate(sentence_tokens)])
    
    print(f"\n[!] Conflict detected for word: '{word}'")
    print(f"  > Sentence: {full_sentence}")
    print(f"              {pointer_line}")
    print(f"    1. spaCy\t[{spacy_pos}]\t{'his, her (ownership)' if spacy_pos == 'PRP$' else 'him, her (subject/ object)' if spacy_pos == 'PRP' else ''}")
    print(f"    2. Stanza\t[{stanza_pos}]\t{'his, her (ownership)' if stanza_pos == 'PRP$' else 'him, her (subject/ object)' if stanza_pos == 'PRP' else ''}")
    
    choice = input(f"\n[?] Use which POS tag for '{word}'? (1 = spaCy [{spacy_pos}], 2 = Stanza [{stanza_pos}]): ").strip()
    return stanza_pos if choice == '2' else spacy_pos

def gender_flip(text: str) -> str:
    spacy_doc = spacy_nlp(text)
    stanza_pos_map = {}  # Lazy load only if needed
    out_tokens = []

    for i, token in enumerate(spacy_doc):
        word = token.text
        lowered = word.lower()

        if lowered in REPLACEMENTS:
            rep = REPLACEMENTS[lowered]

            if isinstance(rep, dict):
                spacy_pos = token.tag_

                if not stanza_pos_map:
                    stanza_pos_map = get_stanza_pos(text)
                stanza_pos = stanza_pos_map.get(word, spacy_pos)

                if spacy_pos != stanza_pos:
                    sentence_tokens = [t.text for t in spacy_doc]
                    final_pos = resolve_conflict(word, spacy_pos, stanza_pos, sentence_tokens, i)
                else:
                    final_pos = spacy_pos

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
    input_text = "As she pinched and squeezed her fully erect nipples, Konomi's body trembled violently as if she was having a convulsion herself."
    result = gender_flip(input_text)
    print("\nFinal Result:")
    print(result)
