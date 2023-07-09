class NameMatch:
    def __init__(self, value, confidence, count=1):
        self.value = value
        self.confidence = confidence
        self.count = count

    def __repr__(self):
        return f"{self.value}:C{self.confidence}#{self.count}"


class NameMatches:
    MATCH_LIMIT = 10
    UNKNOWN_MATCH = "Unknown"

    def __init__(self, matches=None):
        if matches is None:
            matches = {}
        self._matches = matches

    def __add__(self, other):
        matches = self._matches.copy()
        for value, match in other._matches.items():
            if value in matches:
                matches[value].count += match.count
            else:
                matches[value] = match
        return NameMatches(matches)

    def __iter__(self):
        yield from self._matches.values()

    def __repr__(self):
        return str(tuple(str(match) for match in self))

    def add_match(self, match):
        self._matches[match.value] = match

    def get_matches(self):
        matches = list(
            NameMatch(match.value, match.confidence, match.count)
            for match in self._matches.values()
        )

        for small_match in matches:
            if " " in small_match.value:
                for big_match in matches:
                    # can be a problem if multi word lowercase matches
                    if (
                        small_match.value != big_match.value
                        and len(small_match.value) < len(big_match.value)
                        and small_match.value.lower() in big_match.value.lower()
                    ):
                        big_match.confidence += small_match.confidence

        for match in matches:
            match.confidence *= match.count

        matches.sort(key=lambda match: match.confidence, reverse=True)
        matches = matches[: self.MATCH_LIMIT]
        return matches

    def best_match(self, threshold=None):
        matches = self.get_matches()
        return (
            matches[0].value
            if matches
            and (len(matches) == 1 or matches[0].confidence != matches[1].confidence)
            and (not threshold or matches[0].confidence >= threshold)
            else self.UNKNOWN_MATCH
        )
