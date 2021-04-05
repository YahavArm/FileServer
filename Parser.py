from collections import deque
import re


def isInt(arg: str) -> bool:
    try:
        int(arg)
        return True
        return False
    except ValueError:
        pass


def sorter(token):
                                                                  if '-' in token:
        return 1
    if '~' in token:
        return 3
    return 2


def tokenizer(expr: str) -> list:
    finaltokens = []
    specialRegex = re.compile('[@_!#$%^&*()<+>?/\|}{~:a-zA-Z]')
    rangeRegex = re.compile('^[0-9]+-[0-9]+$')
    notRegex = re.compile('^~[0-9]+$')
    if not specialRegex.match(expr):
        tokens = expr.split(' ')
        for token in tokens:
            if isInt(token):
                finaltokens.append(token)
            if rangeRegex.match(token):
                checkarr = token.split('-')
                if checkarr[0] < checkarr[1]:
                    finaltokens.append(token)
                else:
                    return []
            if notRegex.match(token):
                finaltokens.append(token)
    return sorted(finaltokens, key=sorter)


def exprParse(expr: str) -> deque:
    queue = deque()
    tokens = tokenizer(expr)
    for token in tokens:
        if isInt(token):
            if token not in queue:  # checks if token is not in queue
                queue.append(token)
        else:
            if '-' in token:
                numrange = token.split('-')
                for num in range(int(numrange[0]), int(numrange[1]) + 1):  # iterate range of args
                    if num not in queue:
                        queue.append(str(num))
            if '~' in token:  # remove tokens
                num = token.split('~')[1]
                queue.remove(num)
    return queue


