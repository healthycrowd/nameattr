import lxml.etree
import lxml.html.clean

from ._match import NameMatches
from ._text import matches_from_text


def matches_from_html(html):
    cleaner = lxml.html.clean.Cleaner(javascript=True, page_structure=False, style=True)
    html = cleaner.clean_html(html)
    parser = lxml.etree.HTMLParser(
        remove_blank_text=True, remove_comments=True, remove_pis=True
    )
    root = lxml.etree.XML(html, parser)

    result = NameMatches()
    for text in root.itertext():
        result += matches_from_text(text)

    title = root.find(".//title").text.lower()
    for match in result:
        if match.value.lower() in title:
            match.confidence += 0.8

    return result
