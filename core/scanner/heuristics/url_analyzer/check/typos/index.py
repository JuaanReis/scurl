from collections import defaultdict

def build_index(domains: list):

    by_len = defaultdict(list)
    by_first = defaultdict(list)

    for d in domains:
        by_len[len(d)].append(d)
        by_first[d[0]].append(d)

    return by_len, by_first