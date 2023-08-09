
import html
from lib.Lang import Lang, DEFAULT_LANG
from lib.Math import MathSeprate

def MarkdownEscape(s, onlyInlineMath: bool = True):
    s = __ToString(s)
    def e(m):
        tr = {c: "" for c in "\n\r\a\b\t\v\f"}
        tr.update({c: "\\"+c for c in "\\*_`#+-.!{}[]()"})
        tr.update({
            "<": "&lt;",
            ">": "&gt;"
        })
        m = m.translate(str.maketrans(tr)).replace("\\\\$", "\\$")
        return m
    separated = MathSeprate(s, onlyInlineMath = onlyInlineMath)
    # Markdownは数式に対してエスケープをする必要がない
    return "".join([e(elt[0]) + elt[1] for elt in separated])

def HtmlEscape(s, onlyInlineMath: bool = True):
    s = __ToString(s)
    def e(m):
        tr = {c: "" for c in "\n\r\a\b\t\v\f"}
        m = m.translate(str.maketrans(tr))
        return html.escape(m)
    separated = MathSeprate(s, onlyInlineMath = onlyInlineMath)
    # HTMLは数式に対してもエスケープを行う
    return "".join([e(elt[0]) + e(elt[1]) for elt in separated])

# Noneの文字列は str(None) == 'None' ではなく空文字列にしたいので別途関数を定義
def __ToString(s):
    if s is None:
        return ''
    else:
        return str(s)

def Escape(lang: str = DEFAULT_LANG):
    funcs = {
        Lang.md: MarkdownEscape,
        Lang.html: HtmlEscape
    }
    return funcs[Lang.from_str(lang, raiseError = True)]


