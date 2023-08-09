
import re

def __IndexofBlock(s: str, st: int = 0, close: bool = False):
    pattern = r"(?<!\\)\\\]" if close else r"(?<!\\)\\\["
    res = re.search(pattern, s[st:])
    if res is None:
        return -1
    else:
        return res.span()[0] + st
def __IndexofDollarBlock(s: str, st: int = 0):
    res = re.search(r"(?<!\\)\$\$", s[st:])
    if res is None:
        return -1
    else:
        return res.span()[0] + st
def __IndexofInline(s: str, st: int = 0):
    res = re.search(r"(?<!\\)\$", s[st:])
    if res is None:
        return -1
    else:
        return res.span()[0] + st

def __MathSeprate_Block(s: str, idx: int, onlyInlineMath: bool = True):
    st = idx
    ed = __IndexofBlock(s, st + 2, close = True)
    if ed < 0:
        return s, None, None
    head = s[:st]
    math_part = s[st:ed+2]
    if onlyInlineMath:
        math_part = __ToInline(math_part)
    tail = s[ed+2:]
    return head, math_part, tail

def __MathSeprate_DollarBlock(s: str, idx: int, onlyInlineMath: bool = True):
    st = idx
    ed = __IndexofDollarBlock(s, st + 2)
    if ed < 0:
        return s, None, None
    head = s[:st]
    math_part = s[st:ed+2]
    if onlyInlineMath:
        math_part = __ToInline(math_part)
    tail = s[ed+2:]
    return head, math_part, tail

def __MathSeprate_Inline(s: str, idx: int):
    st = idx
    ed = __IndexofInline(s, st + 1)
    if ed < 0:
        return s, None, None
    head = s[:st]
    math_part = s[st:ed+1]
    tail = s[ed+1:]
    return head, math_part, tail

def __ToInline(s: str):
    return f"${s[2:-2].strip()}$"

# 数式とそうでない部分とに分け，ついでにブロック数式をインライン数式に修正する(description以外)
# 数式の部分だけエスケープしないといった処理を行うため．
def MathSeprate(s: str, onlyInlineMath: bool = True):
    dollar_idx = __IndexofInline(s)
    bracket_idx = __IndexofBlock(s)
    if dollar_idx < 0 and bracket_idx < 0:
        return [[s, '']]
    dollar_first = bracket_idx < 0 or (0 <= dollar_idx and dollar_idx < bracket_idx)
    if dollar_first:
        dollarblock_idx = __IndexofDollarBlock(s)
        if dollarblock_idx == dollar_idx:
            head, math_part, tail = __MathSeprate_DollarBlock(s, dollarblock_idx, onlyInlineMath = onlyInlineMath)
        else:
            head, math_part, tail = __MathSeprate_Inline(s, dollar_idx)
    else:
        head, math_part, tail = __MathSeprate_Block(s, bracket_idx, onlyInlineMath = onlyInlineMath)
    if math_part is None:
        return [[head, '']]
    else:
        return [[head, math_part]] + MathSeprate(tail, onlyInlineMath = onlyInlineMath)

