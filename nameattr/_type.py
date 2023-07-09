import re
from collections import OrderedDict


def word_starts_lower(value):
    return is_name(value) and value[0].lower() == value[0]


def word_starts_upper(value):
    return is_name(value) and value[0].upper() == value[0]


def is_name(value):
    return bool(re.match("^\\w+[_\\w]+$", value))


class NameType:
    def __init__(self, word_matches, confidence):
        self.word_matches = word_matches
        self.confidence = confidence


# Change from dict to tuple
NAME_TYPES = OrderedDict(
    {
        "FULL_SINGLE_PREFIXED_SURNAME": NameType(
            (word_starts_upper, word_starts_lower, word_starts_upper), 0.6
        ),
        "FULL_DOUBLE_PREFIXED_SURNAME": NameType(
            (
                word_starts_upper,
                word_starts_lower,
                word_starts_lower,
                word_starts_upper,
            ),
            0.5,
        ),
        "FULLNAME_MIDDLE": NameType((word_starts_upper,) * 3, 0.4),
        "FULLNAME": NameType((word_starts_upper,) * 2, 0.3),
        "MONONYM": NameType((word_starts_upper,), 0.2),
    }
)


def confidence_by_type(words):
    for name_type in NAME_TYPES.values():
        if not len(words) == len(name_type.word_matches):
            continue
        try:
            if all(
                match_func(words[match_index])
                for (match_index, match_func) in enumerate(name_type.word_matches)
            ):
                return name_type.confidence
        except IndexError:
            continue

    return 0.1
