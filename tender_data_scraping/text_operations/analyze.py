import re


def find_search_words(string):
    """
    Search a given string for words related to TCO certified
    :param string: a string
    :return: found words
    """
    no_case_sensitivity = ["energy", "efficiency", "environment", "environmental", "sustainability", "lifecycle",
                           "ergonomic", "ecological", "circular economy", "tco", "epeat", "nachhaltigkeit", "Umwelt",
                           "Kreislaufwirtschaft", "Ergonomie", "EU", "GPP"]
    check_after = ["epeat", "energy", "tco"]
    find_exact = ["ROHS", "EPR", "BEE star", "TCO"]

    word_list = []
    matches_list = []
    no_case_words = []
    check_after_words = []
    find_exact_word = []

    for word in no_case_sensitivity:
        no_case_words.append(re.findall(r"\b({})(\w+|)".format(word), string, flags=re.IGNORECASE))

    for word in check_after:
        check_after_words.append(re.findall(r"\b({})( |-|.)(\w+)".format(word), string, flags=re.IGNORECASE))

    for word in find_exact:
        find_exact_word.append(re.findall(r"(?<!\w)({})(\w+|)".format(word), string))

    matches_list = matches_list + no_case_words + check_after_words + find_exact_word

    print("Matches found:", matches_list)

    for match_list in matches_list:
        for match in match_list:
            try:
                word_list.append(match[0] + " " + match[-1])
            except Exception:
                pass
    print("Words found:", word_list)

    if len(word_list) == 0:
        words = None
    else:
        words = list(set(word_list))
    return words


interesting_words = ["energy", "efficiency", "environment", "environmental", "tco", "sustainability", "sustainable",
                     "life", "cycle", "ergonomic", "eco", "ecological", "circular", "economy", "circulaire", "economie",
                     "certification", "certificate", "EU", "GPP"]


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


def analyze(text):
    print(text)
    search = {"TCO": None, "EPEAT": None}
    # Find if TCO is mentioned
    TCO_item = find_text(text, r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
    search["TCO"] = TCO_item

    # Find if EPEAT is mentioned
    EPEAT_item = find_text(text, r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
    search["EPEAT"] = EPEAT_item
    return search


def find_text(text, regex):
    try:
        matchobj = re.search(regex, str(text(text=(re.compile(regex)))))
    except TypeError:
        matchobj = re.search(regex, text)
    if matchobj:
        item = matchobj.group()
    else:
        item = None
    return item