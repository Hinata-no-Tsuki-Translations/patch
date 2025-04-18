import spacy

nlp = spacy.load("en_core_web_sm")

# Mapping from feminine to masculine pronouns and reflexive forms
REPLACEMENTS = {
    "her":      {"PRP$": "his",  "PRP": "him"},   # PRP$=possessive, PRP=personal
    "hers":     "his",                         # possessive pronoun
    "herself":  "himself",                     # reflexive
    "she":      "he",                           # subject pronoun
}

def gender_flip(text: str) -> str:
    doc = nlp(text)
    out_tokens = []
    for token in doc:
        low = token.text.lower()
        # only consider known feminine forms
        if low in REPLACEMENTS:
            rep = REPLACEMENTS[low]
            # skip if this token is part of a named entity you want to preserve
            if token.ent_type_:
                out = token.text
            else:
                if isinstance(rep, dict):
                    # choose replacement based on tag (PRP$ vs PRP)
                    out = rep.get(token.tag_, token.text)
                else:
                    out = rep
            # match capitalization
            if token.text[0].isupper():
                out = out.capitalize()
            out_tokens.append(out + token.whitespace_)
        else:
            out_tokens.append(token.text_with_ws)
    return "".join(out_tokens)

# Example
s = "She was walking to her car. Her book is on the table."
print(gender_flip(s))
# "He was walking to his car. His book is on the table."
