
from lib.Escape import Escape
from lib.Lang import Lang, DEFAULT_LANG
from lib.BookType import BookType

def BookFormat_markdown(info):
    if info.URL is None:
        title = info.title
    else:
        title = f"[{info.title}]({info.URL})"
    title = f"“{title}”"
    if not info.author is None:
        title = f"{info.author}, {title}"
    if not info.publisher is None:
        title = f"{title}, {info.publisher}"
    title = f"- ({info.alias}): {title}"
    if not info.year is None:
        title += f", {info.year}"
    added = []
    if not info.path is None:
        added.append(f"\n\t- パス: {info.path}")
    if not info.description is None:
        if type(info.description) == list:
            descs = "\n".join([f"\t- {d}" for d in info.description])
        else:
            descs = f"\t- {info.description}"
        added.append(f"\n{descs}")
    if not info.related is None:
        if type(info.related) == list:
            related = "\n".join([f"\t\t- {r}" for r in info.related])
            related = f"\n\t- 関連：\n{related}"
        else:
            related = f"\n\t- 関連：{info.related}"
        added.append(related)
    if info.type == BookType.book and not info.ISBN is None:
        added.append(f"\n\t- ISBN: {info.ISBN}")
    if info.type == BookType.paper and not info.DOI is None:
        added.append(f"\n\t- DOI: {info.DOI}")
    if info.type == BookType.website and not info.last_accessed is None:
        added.append(f"\n\t- 最終アクセス: {info.last_accessed}")
    return title + "".join(added)

def BookFormat_html(info):
    if info.URL is None:
        title = info.title
    else:
        title = f"<a href='{info.URL}'>{info.title}</a>"
    title = f"“{title}”"
    if not info.author is None:
        title = f"{info.author}, {title}"
    if not info.publisher is None:
        title = f"{title}, {info.publisher}"
    title = f"({info.alias}): {title}"
    if not info.year is None:
        title += f", {info.year}"
    added = []
    if not info.path is None:
        added.append(f"\n\t<li>パス: {info.path}</li>")
    if not info.description is None:
        if type(info.description) == list:
            descs = "\n".join([f"\t<li>{d}</li>" for d in info.description])
        else:
            descs = f"\t<li>{info.description}</li>"
        added.append(f"\n{descs}")
    if not info.related is None:
        if type(info.related) == list:
            related = "\n".join([f"\t\t<li>{r}</li>" for r in info.related])
            related = f"\n\t<li>関連：\n\t<ul>\n{related}\n\t</ul></li>"
        else:
            related = f"\n\t<li>関連：{info.related}</li>"
        added.append(related)
    if info.type == BookType.book and not info.ISBN is None:
        added.append(f"\n\t<li>ISBN: {info.ISBN}</li>")
    if info.type == BookType.paper and not info.DOI is None:
        added.append(f"\n\t<li>DOI: {info.DOI}</li>")
    if info.type == BookType.website and not info.last_accessed is None:
        added.append(f"\n\t<li>最終アクセス: {info.last_accessed}</li>")
    if len(added) > 0:
        return f"<li>{title}\n\t<ul>{''.join(added)}\n\t</ul></li>"
    else:
        return f"<li>{title}</li>"

def BookFormat(lang: str = DEFAULT_LANG):
    funcs = {
        Lang.md: BookFormat_markdown,
        Lang.html: BookFormat_html
    }
    return funcs[Lang.from_str(lang, raiseError = True)]


def __WordFormat_BookAliasAndRef_markdown(alias: str, ref: list):
    refs = '/'.join(ref)
    return f"{alias}\\[{refs}\\]"

def WordFormat_markdown(info):
    if info.aliases is None:
        refs = [__WordFormat_BookAliasAndRef_markdown(info.book_aliases[i], info.ref[i]) for i in range(len(info.book_aliases))]
        title = f"- {info.disp} ({', '.join(refs)})"
        if not info.desc is None:
            desc = [f"({__WordFormat_BookAliasAndRef_markdown(d['book_alias'], d['ref'])}) {d['desc']}" for d in info.desc]
            descs = "\n".join([f"\t- {d}" for d in desc])
            title += f"\n{descs}"
    else:
        title = f"- {info.disp} -> {', '.join(info.aliases)}"
    return title

def __WordFormat_BookAliasAndRef_html(alias: str, ref: list):
    refs = '/'.join(ref)
    return f"{alias}[{refs}]"

def WordFormat_html(info):
    if info.aliases is None:
        refs = [__WordFormat_BookAliasAndRef_html(info.book_aliases[i], info.ref[i]) for i in range(len(info.book_aliases))]
        has_desc = not info.desc is None
        classname = 'has_desc' if has_desc else ''
        if has_desc:
            desc = [f"({__WordFormat_BookAliasAndRef_html(d['book_alias'], d['ref'])}) {d['desc']}" for d in info.desc]
            descs = "\n".join([f"<li>{d}</li>" for d in desc])
            title = f"<li><details><summary>{info.disp} ({', '.join(refs)})</summary><ul>{descs}</ul></details></li>"
        else:
            title = f"<li>{info.disp} ({', '.join(refs)})</li>"
    else:
        title = f"<li>{info.disp} -&gt; {', '.join(info.aliases)}</li>"
    return title

def WordFormat(lang: str = DEFAULT_LANG):
    funcs = {
        Lang.md: WordFormat_markdown,
        Lang.html: WordFormat_html
    }
    return funcs[Lang.from_str(lang, raiseError = True)]

