
from textwrap import dedent
from lib.Lang import Lang, DEFAULT_LANG
from lib.TeXMacro import HTML_TeXMacros

HTML_BIB_ID = "bib"

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,100,1,200" />
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
li.word.hidden{{
    display: none;
}}
li.word a.book-link{{
    color: inherit;
    text-decoration: none;
}}
li.word span.ref.hidden{{
    opacity: 0.3;
}}
li.book span.visibility{{
	display: inline-block;
	width: 1em;
	height: 1em;
	cursor: pointer;
	vertical-align: middle;
}}
li.book span.visibility.off{{
	opacity: 0.3;
}}
</style>
<script>
function word_reset_visibility(){{
	const visible_book_ids = Array.from(document.getElementsByClassName('book'))
	.filter(book => !book.getElementsByClassName('visibility')[0].classList.contains('off'))
	.map(book => book.id);

	Array.from(document.getElementsByClassName('word'))
	.forEach(word => {{
		if(visible_book_ids.every(book_id => !word.classList.contains(book_id))){{
			word.classList.add('hidden');
		}}else{{
			word.classList.remove('hidden');
			Array.from(word.getElementsByClassName('ref'))
			.forEach(ref => {{
				if(visible_book_ids.some(book_id => ref.classList.contains(book_id))){{
					ref.classList.remove('hidden');
				}}else{{
					ref.classList.add('hidden');
				}}
			}});
		}}
	}});
}}
function reset_visibility_text(){{
	Array.from(document.getElementsByClassName('visibility')).forEach(e => {{
        if(e.classList.contains('off')){{
            e.innerText = 'visibility_off';
        }}else{{
            e.innerText = 'visibility';
        }}
    }});
}}
function toggle_visibility(e){{
	e.classList.toggle('off');
}}
function is_only_one_visible(e){{
    return !e.classList.contains('off') &&
    Array.from(document.getElementsByClassName('visibility'))
    .every(el => e === el || el.classList.contains('off'));
}}
function set_only_one_visible(e){{
	Array.from(document.getElementsByClassName('visibility')).forEach(el => {{
		el.classList.add('off');
	}});
	e.classList.remove('off');
}}
function set_all_visible(){{
    Array.from(document.getElementsByClassName('visibility'))
    .forEach(e => e.classList.remove('off'));
}}
document.addEventListener('DOMContentLoaded', () => {{
	Array.from(document.getElementsByClassName('visibility'))
	.forEach(el => {{
		el.addEventListener('click', () => {{
			toggle_visibility(el);
			word_reset_visibility();
            reset_visibility_text();
		}});
		el.addEventListener('contextmenu', e => {{
			e.preventDefault();
            if(is_only_one_visible(el)){{
                set_all_visible();
            }}else{{
                set_only_one_visible(el);
            }}
			word_reset_visibility();
            reset_visibility_text();
		}});
	}});
}});
</script>
</head>
<body>
<h1>索引</h1>
<ul style="display: none">
        """,
        "headchar": "\n</ul>\n\n<h3 id='{id}'>{char}</h3>\n<ul>\n\n",
        "books": f"\n</ul>\n<h2 id='{HTML_BIB_ID}'>文献一覧</h2>\n<ul>\n\n",
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
        # [表示文字列, 比較文字, HTML用ID]
        ["記号・数式", "$", "$"],
        ["数字", "0", "0"]
    ] + [
        [chr(i), chr(i), chr(i)] for i in range(65, 91) # 大文字英字
    ] + [
        ["あ", "ぁ", "あ"]
    ] + [
        [c, c, c] for c in "かさたなはま"
    ] + [
        ["や", "ゃ", "や"], ["ら", "ら", "ら"], ["わ", "ゎ", "わ"]
    ]
    __next_idx = 0
    @staticmethod
    def apply(outfile, word, lang: str):
        i = HeadChar.__next_idx
        if i >= len(HeadChar.__chars):
            return
        newlabel, newchar, newid = HeadChar.__chars[i]
        if i == 0 or newchar <= word.head():
            outfile.write(RemoveIndent(HeadersFromLang(lang)['headchar']).format(char = newlabel, id = newid))
            HeadChar.__next_idx += 1
            HeadChar.apply(outfile, word, lang)
    @staticmethod
    def getIDs():
        return [c[2] for c in HeadChar.__chars]

