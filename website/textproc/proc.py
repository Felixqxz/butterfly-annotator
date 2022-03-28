from itertools import permutations, takewhile

from website.database.models import UserSelectedKeyword
from ..database.access import db
from sqlalchemy import and_
import os


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


# add keywords if it is not in the bound of user_keywords_selection list
def add_keywords(start_index, end_index, user_keywords, keywords):
    not_in_bound = True
    for keyword in user_keywords:
        if keyword['start'] <= start_index <= keyword['end'] or \
                keyword['start'] <= end_index <= keyword['end']:
            not_in_bound = False
            break
    if not_in_bound:
        keywords.append({'start': start_index, 'end': end_index})


def get_keywords(adjectives, patterns, description, image_bank_id):
    keywords = []
    user_keywords = []
    i = 0

    user_keywords_list = db.session.query(UserSelectedKeyword) \
        .filter(and_(UserSelectedKeyword.image_bank_id == image_bank_id)) \
        .all()

    for user_keyword in user_keywords_list:
        user_keyword = user_keyword.keyword
        start_index = description.lower().find(user_keyword)
        if start_index != -1:
            end_index = start_index + len(user_keyword)
            add_keywords(start_index, end_index, user_keywords, user_keywords)

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
                end_index = i + len(word)
                add_keywords(start_index, end_index, user_keywords, keywords)
                start_index = -1
            i += len(word)
        elif (curr == ';' or curr == '.') and start_index != -1:
            # termination!
            end_index = i
            add_keywords(start_index, end_index, user_keywords, keywords)
            start_index = -1
            i += 1
        else:
            i += 1
    all_keywords = user_keywords + keywords
    return all_keywords
