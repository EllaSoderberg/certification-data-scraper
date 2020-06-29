import re


def find_search_words(string):
    """
    Search a given string for words related to TCO certified
    :param string: a string
    :return: found words
    """
    no_case_sensitivity = ["energy", "efficiency", "environment", "environmental", "sustainability", "lifecycle",
                           "ergonomic", "ecological", "circular economy", "tco", "epeat", "nachhaltigkeit", "Umwelt",
                           "Kreislaufwirtschaft", "Ergonomie"]
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
