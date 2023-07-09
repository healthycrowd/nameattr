import pytest

import nameattr
from nameattr._match import NameMatches
from .names import (
    MONONYM,
    FULLNAME,
    FULLNAME_MIDDLE,
    FULL_DOUBLE_PREFIXED_SURNAME,
    FULL_SINGLE_PREFIXED_SURNAME,
)


@pytest.mark.parametrize(
    "text,expected",
    [
        (f"{MONONYM} is the subject of this sentence.", MONONYM),
        (f"{FULLNAME} is the subject of this sentence not {MONONYM}.", FULLNAME),
        (
            f"{FULLNAME_MIDDLE} is the subject of this sentence not {MONONYM} or {FULLNAME}.",
            FULLNAME_MIDDLE,
        ),
        (
            f"{FULL_DOUBLE_PREFIXED_SURNAME} is the subject of this sentence not {MONONYM} or {FULLNAME} or {FULLNAME_MIDDLE}",
            FULL_DOUBLE_PREFIXED_SURNAME,
        ),
        (
            f"{FULL_SINGLE_PREFIXED_SURNAME} is the subject of this sentence not {MONONYM} or {FULLNAME} or {FULLNAME_MIDDLE} or {FULL_DOUBLE_PREFIXED_SURNAME}",
            FULL_SINGLE_PREFIXED_SURNAME,
        ),
    ],
)
def test_text_faked(text, expected):
    assert nameattr.from_text(text) == expected, nameattr.matches_from_text(text)


@pytest.mark.skip()
@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "Original Art Digital Printmaking, measuring: 50.8W x 67.06H x 0.25D cm, by: Fadhel Dabbagh (United States). Styles: Modern. Subject: Nature. Keywords: New World, Modern Art, Art, Peace, Collage, Happy Land, Abstract Painting, Painting, Peace Land, Flower, Digital Art, Art Work. This Digital Printmaking is one of a kind and once sold will no longer be available to purchase. Buy art at Saatchi Art.",
            "Fadhel Dabbagh",
        ),
        ("contemporaryfibers:  Diana Nagorna.", "Diana Nagorna"),
        (
            "Trochaic Symbol - Živojin Turinski - Yugoslav Modern Art - National Museum Belgrade",
            "Živojin Turinski",
        ),
        (
            "Artist Spotlight: Niv Bavarsky – BOOOOOOOM! – CREATE * INSPIRE * COMMUNITY * ART * DESIGN * MUSIC * FILM * PHOTO * PROJECTS",
            "Niv Bavarsky",
        ),
        ("Soul in the Water, Russell Tomlin", "Russell Tomlin"),
        (
            "Photographer Spotlight: Adriana Roslin – BOOOOOOOM! – CREATE * INSPIRE * COMMUNITY * ART * DESIGN * MUSIC * FILM * PHOTO * PROJECTS",
            "Adriana Roslin",
        ),
        ("The perfect witch house in forbidden forest , Poland …", "Poland"),
        (
            "2022 Booooooom Photo Awards Winner: Ophélie Maurus – BOOOOOOOM! – CREATE * INSPIRE * COMMUNITY * ART * DESIGN * MUSIC * FILM * PHOTO * PROJECTS",
            "Ophélie Mauruus",
        ),
        (
            "Artist Spotlight: Hamadaraka – BOOOOOOOM! – CREATE * INSPIRE * COMMUNITY * ART * DESIGN * MUSIC * FILM * PHOTO * PROJECTS",
            "Hamadaraka",
        ),
    ],
)
def test_text_real(text, expected):
    assert nameattr.from_text(text) == expected, nameattr.matches_from_text(text)


def test_text_threshold():
    text = f"{MONONYM} is the subject of this sentence."
    name = MONONYM
    assert nameattr.from_text(text) == name
    assert (
        nameattr.from_text(text, threshold=1) == NameMatches.UNKNOWN_MATCH
    ), nameattr.matches_from_text(text)
