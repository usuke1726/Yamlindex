
from textwrap import dedent
from lib.Lang import Lang, DEFAULT_LANG
from lib.TeXMacro import HTML_TeXMacros

__Headers = {
    Lang.md: {
        "top": "\n\n## 索引\n\n\n",
        "headchar": "\n\n### {char}\n\n\n",
        "books": "\n\n\n## 文献一覧\n\n\n",
        "bottom": "\n\n\n"
    },
    Lang.html: {
        "top": """
<!DOCTYPE html>
<html lang="ja">
<head>
<title>索引</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.css" integrity="sha384-yFRtMMDnQtDRO8rLpMIKrtPCD5jdktao2TV19YiZYWMDkUR5GQZR/NOVTdquEx1j" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.js" integrity="sha384-9Nhn55MVVN0/4OFx7EE5kpFBPsEMZxKTCnA+4fqDmg12eCTqGi6+BB2LjY8brQxJ" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous" onload="renderMathInElement(document.body);"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {{
renderMathInElement(
document.body, {{
    delimiters: [
        {{ left: "\\\\[", right: "\\\\]", display: true }},
        {{ left: "$$", right: "$$", display: true }},
        {{ left: "$", right: "$", display: false }}
    ],
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
    errorCallback: console.error,
    macros: {macros}
}})
for (e of document.getElementsByClassName("sample-code")) {{
var editor = ace.edit(e);
editor.setOption("maxLines", "Infinity");
editor.setReadOnly(true);
editor.getSession().setMode("ace/mode/c_cpp");                
}}
}});
</script>
<style>
body{{
    overflow-wrap: anywhere
}}
details{{
    display: inline-block;
}}
summary{{
    list-style: none;
    cursor: pointer;
    width: fit-content;
}}
summary::after{{ margin-left: 5px; }}
details:not([open]) summary::after{{ content: '▶'; }}
details[open] summary::after{{ content: '▼'; }}
a.book-link{{
    color: inherit;
    text-decoration: none;
}}
</style>
</head>
<body>
<h1>索引</h1>
<ul style="display: none">
        """,
        "headchar": "\n</ul>\n\n<h3 id='{id}'>{char}</h3>\n<ul>\n\n",
        "books": "\n</ul>\n<h2 id='bib'>文献一覧</h2>\n<ul>\n\n",
        "bottom": """
            </ul>
            </body>
            </html>

        """
    }
}

def HeadersFromLang(lang: str):
    return __Headers[Lang.from_str(lang, raiseError = True)]

def RemoveIndent(s: str):
    return dedent(s)[1:-1]

def __write(f, lang: str, key: str):
    return f.write(RemoveIndent(HeadersFromLang(lang)[key]))

def PrintTopHeader(f, lang: str = DEFAULT_LANG):
    data = HTML_TeXMacros()
    l = Lang.from_str(lang)
    __Headers[l]['top'] = __Headers[l]['top'].format(macros = data)
    __write(f, lang, 'top')

def PrintBookHeader(f, lang: str = DEFAULT_LANG):
    __write(f, lang, 'books')

def PrintFooter(f, lang: str = DEFAULT_LANG):
    __write(f, lang, 'bottom')

# セクション見出しを適切なタイミングで出力していく静的クラス
class HeadChar:
    __chars = [
        # [表示文字列, 比較文字]
        ["記号・数式", "$"],
        ["数字", "0"]
    ] + [
        [chr(i), chr(i)] for i in range(65, 91) # 大文字英字
    ] + [
        ["あ", "ぁ"]
    ] + [
        [c, c] for c in "かさたなはま"
    ] + [
        ["や", "ゃ"], ["ら", "ら"], ["わ", "ゎ"]
    ]
    __next_idx = 0
    @staticmethod
    def apply(outfile, word, lang: str):
        i = HeadChar.__next_idx
        if i >= len(HeadChar.__chars):
            return
        newlabel, newchar = HeadChar.__chars[i]
        if i == 0 or newchar <= word.head():
            outfile.write(RemoveIndent(HeadersFromLang(lang)['headchar']).format(char = newlabel, id = newchar))
            HeadChar.__next_idx += 1
            HeadChar.apply(outfile, word, lang)

