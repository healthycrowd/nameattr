import nltk

from ._match import NameMatch, NameMatches
from ._type import confidence_by_type, is_name


"""
Would be nice to get rid of this since these will change over time
Could maybe use information in HTML implementaton to replace this
Domain name can't be used in URL implementation since it can contain a name
"""
IGNORELIST = (
    "facebook",
    "youtube",
    "whatsapp",
    "instagram",
    "tiktok",
    "snapchat",
    "pinterest",
    "reddit",
    "linkedin",
    "twitter",
    "flickr",
    "tumblr",
)


def matches_from_text(text):
    result = NameMatches()
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [text]

    for sentence in sentences:
        matches = NameMatches()
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        # Tag list: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        index = 0
        while index < len(tagged):
            (token, tag) = tagged[index]
            if (
                tag in ("NNP", "NNPS")
                and token.lower() not in IGNORELIST
                and is_name(token)
            ):
                value = [token]
                while index < len(tagged) - 1:
                    (token, tag) = tagged[index + 1]
                    if tag in ("NNP", "NNPS", "NN", "CC") and len(token) > 1:
                        value.append(token)
                        index += 1
                    else:
                        break

                confidence = confidence_by_type(value)
                value = " ".join(value)
                matches.add_match(NameMatch(value, confidence))
            index += 1
        result += matches

    return result
