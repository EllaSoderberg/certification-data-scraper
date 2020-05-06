import re

interesting_words = ["energy", "efficiency", "environment", "environmental", "tco", "sustainability", "sustainable",
                     "life", "cycle", "ergonomic", "eco", "ecological", "circular", "economy", "circulaire", "economie",
                     "certification", "certificate"]


def analysis(string):
    word_list = []
    for word in interesting_words:
        try:
            criteria = string.lower()
            found_words = re.findall(r"({})(\w+|[ -]\w+)".format(word), criteria)
            if len(found_words) == 0:
                if word in criteria.lower():
                    word_list.append(word)
            for found in found_words:
                word_list.append(found[0] + found[1])
        except Exception:
            pass

    if len(word_list) == 0:
        words = None
    else:
        words = str(word_list).strip("[").strip("]")
    return words
