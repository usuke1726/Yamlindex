
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
        if type(info.path) == list:
            pathes = "\n".join([f"\t\t- {p}" for p in info.path])
            added.append(f"\n\t- パス：\n{pathes}")
        else:
            added.append(f"\n\t- パス：{info.path}")
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
        if type(info.path) == list:
            pathes = "\n".join([f"\t\t<li>{p}</li>" for p in info.path])
            added.append(f"\n\t<li>パス：\n\t<ul>\n{pathes}\n\t</ul></li>")
        else:
            added.append(f"\n\t<li>パス：{info.path}</li>")
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
    attributes = f"class='book' id='{info.id}'"
    visibility_icon = "<span class='visibility material-symbols-outlined'>visibility</span>"
    if len(added) > 0:
        return f"<li {attributes}>{visibility_icon}{title}\n\t<ul>{''.join(added)}\n\t</ul></li>"
    else:
        return f"<li {attributes}>{visibility_icon}{title}</li>"

def BookFormat(lang: str = DEFAULT_LANG):
    funcs = {
        Lang.md: BookFormat_markdown,
        Lang.html: BookFormat_html
    }
    return funcs[Lang.from_str(lang, raiseError = True)]


def __WordFormat_BookAliasAndRef_markdown(alias: str, ref: list):
    if ref is None:
        refs = ""
    else:
        refs = f"\\[{'/'.join(ref)}\\]"
    return f"{alias}{refs}"

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

def __WordFormat_BookAliasAndRef_html(alias: str, ref: list, book_id: str):
    if ref is None:
        refs = ""
    else:
        valid_ref = [r for r in ref if len(r.strip()) > 0]
        if len(valid_ref) > 0:
            refs = f"[{'/'.join(valid_ref)}]"
        else:
            refs = ""
    if book_id is None:
        return f"{alias}{refs}"
    else:
        return f"<span class='ref {book_id}'><a class='book-link' href='#{book_id}'>{alias}</a>{refs}</span>"

def WordFormat_html(info):
    if info.aliases is None:
        refs = [__WordFormat_BookAliasAndRef_html(info.book_aliases[i], info.ref[i], info.book_ids[i]) for i in range(len(info.book_aliases))]
        has_desc = not info.desc is None and len(info.desc) > 0
        classname = 'has_desc' if has_desc else ''
        if has_desc:
            desc = [f"({__WordFormat_BookAliasAndRef_html(d['book_alias'], d['ref'], None)}) {d['desc']}" for d in info.desc]
            descs = "\n".join([f"<li>{d}</li>" for d in desc])
            body = f"<details><summary>{info.disp} ({', '.join(refs)})</summary><ul>{descs}</ul></details>"
        else:
            body = f"{info.disp} ({', '.join(refs)})"
    else:
        body = f"{info.disp} -&gt; {', '.join(info.aliases)}"
    body = f"<li class='word {' '.join(info.book_ids)}'>{body}</li>"
    return body

def WordFormat(lang: str = DEFAULT_LANG):
    funcs = {
        Lang.md: WordFormat_markdown,
        Lang.html: WordFormat_html
    }
    return funcs[Lang.from_str(lang, raiseError = True)]

