import urllib.request
import urllib.error
import urllib.parse

from ._html import matches_from_html


URL_PARTS = (
    ("hostname", 0.8),
    ("path", 0.6),
    ("fragment", 0.5),
    ("query", 0.4),
)


def matches_from_url(url, html=None):
    if html is None:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla",
            },
        )
        html = urllib.request.urlopen(request).read().decode()

    result = matches_from_html(html)

    match_url = url.lower()
    parsed_url = urllib.parse.urlparse(match_url)
    for match in result:
        words = match.value.lower().split(" ")

        for attr, confidence in URL_PARTS:
            match_part = getattr(parsed_url, attr)
            if all(word in match_part for word in words):
                match.confidence += confidence
                break
        else:
            if any(word in match_url for word in words):
                match.confidence += 0.4

    return result
