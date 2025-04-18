import spacy

nlp = spacy.load("en_core_web_sm")

# mapping from (lowercase) feminine form Å® masculine
REPLACEMENTS = {
    "her":      {"PRP$": "his",  "PRP": "him"},   # PRP$=possessor, PRP=personal
    "hers":     "his",                         # possessive pronoun
    "herself":  "himself",                     # reflexive
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
                    # choose by tag_ (PRP$ vs PRP)
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
s = "Her running down the street was noticed by everyone. I gave her book to the library."
print(gender_flip(s))
# Å® "His running down the street was noticed by everyone. I gave him book to the library."
