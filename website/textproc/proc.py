from itertools import takewhile

def get_keywords(adjectives, patterns, description):
    keywords = []
    word = None
    start_index = -1
    i = 0
    while i < len(description):
        curr = description[i]
        # beginning of a word
        if curr.isalpha():
            word = ''.join(list(takewhile(lambda c: c.isalpha() or c == '-', description[i:]))).lower()
            # potential beginning of a description
            if word in adjectives and start_index == -1:
                start_index = i
            elif word in patterns and start_index != -1:
                keywords.append({'start': start_index, 'end': i + len(word)})
                start_index = -1
            i += len(word)
        elif (curr == ';' or curr == '.') and start_index != -1:
            # termination!
            keywords.append({'start': start_index, 'end': i})
            start_index = -1
            i += 1
        else:
            i += 1
    return keywords
