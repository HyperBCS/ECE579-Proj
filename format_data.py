import sys

subreddits = {}

with open('data.txt') as f:
    lines = f
    for l in lines.readlines():
        dat = l.split('\t')
        if dat[0] not in subreddits:
            subreddits[dat[0]] = []