from itertools import takewhile

import os

USER_KEYWORDS_SELECTION_PATH = os.path.join(os.getcwd(), 'termlist', 'user_keywords_selection.txt')

def load_word_list(p):
    """
    Loads a list of provided words.
    """
    ls = []
    if os.path.isfile(p):
        with open(p, 'r') as file:
            lines = file.readlines()
            for line in lines:
                ls.append(line.strip().lower())
    return ls

user_keywords_list = load_word_list(USER_KEYWORDS_SELECTION_PATH)

def get_keywords(adjectives, patterns, description):
    keywords = []
    user_keywords = []
    word = None
    start_index = -1
    i = 0
    for user_keyword in user_keywords_list:
        start_index = description.find(user_keyword)
        if start_index != -1:
            user_keywords.append({'start': start_index, 'end': start_index + len(user_keyword)})

    start_index = -1
    while i < len(description):
        curr = description[i]
        # beginning of a word
        if curr.isalpha():
            word = ''.join(list(takewhile(lambda c: c.isalpha() or c == '-', description[i:]))).lower()
            # potential beginning of a description
            if word in adjectives and start_index == -1:
                start_index = i
            elif word in patterns and start_index != -1:
                not_in_bound = True
                end_index = i + len(word)
                for user_keyword in user_keywords:
                    if start_index >= user_keyword['start'] and start_index <= user_keyword['end'] or \
                        end_index >= user_keyword['start'] and end_index <= user_keyword['end']:
                        not_in_bound = False
                        break
                
                if not_in_bound:
                    keywords.append({'start': start_index, 'end': i + len(word)})
                start_index = -1
            i += len(word)
        elif (curr == ';' or curr == '.') and start_index != -1:
            # termination!
            not_in_bound = True
            end_index = i
            for user_keyword in user_keywords:
                if start_index >= user_keyword.start and start_index <= user_keyword.end or \
                    end_index >= user_keyword.start and end_index <= user_keyword.end:
                    not_in_bound = False
                    break
            if not_in_bound:
                keywords.append({'start': start_index, 'end': i})
            start_index = -1
            i += 1
        else:
            i += 1
    return user_keywords + keywords
