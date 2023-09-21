
from lib.Hiragana import ToHiragana
from lib.TmpFiles import TmpFiles
from lib.Word import Word
from lib.Log import Progress, Log

class WordDataError(Exception):
    pass

def __DictNum(data):
    def num(e):
        if type(e) == list:
            return len(e)
        else:
            return 1
    nondict_num = sum([num(v) for v in data.values() if type(v) != dict])
    subdict_keys = [k for k in data.keys() if type(data[k]) == dict]
    return nondict_num + sum([__DictNum(data[k]) for k in subdict_keys])

# Yamlファイルを読んで索引語データを逐次出力していく
def ReadDict(data: dict, book_alias: str, book_id: str):
    n = __DictNum(data)
    if n == 0:
        Log(f"索引語が1つもありません ({book_alias})")
        return
    with Progress(n, f"ReadDict: {book_alias} ({book_id})") as prog:
        __ReadDict_proc(prog, data, book_alias, book_id, [])

def __ReadDict_proc(prog, data: dict, book_alias: str, book_id: str, ref: list):
    for k, v in data.items():
        k = str(k)
        new_ref = ref + [k]
        if type(v) == dict:
            __ReadDict_proc(prog, v, book_alias, book_id, new_ref)
        elif type(v) == list:
            if len(v) == 0:
                Log(f"索引語が指定されていません: {k} ({book_alias}[{'/'.join(ref)}])")
            for row in v:
                try:
                    if type(row) == dict:
                        __ReadDict_proc(prog, row, book_alias, book_id, new_ref)
                    else:
                        __AppendWord(row, book_alias, book_id, new_ref)
                        prog.step()
                except WordDataError as e:
                    Log(f"Word error at {row}: {e}")
        elif v is None:
            Log(f"索引語が指定されていません: {k} ({book_alias}[{'/'.join(ref)}])")
        else:
            Log(f"型が辞書型でもリストでもありません: {v} {type(v)} ({book_alias}[{'/'.join(ref)}])")

def __AppendWord(row, book_alias: str, book_id: str, ref: list):
    if type(row) == str:
        __AppendWord_str(row, book_alias, book_id, ref)
    elif type(row) == list:
        __AppendWord_list(row, book_alias, book_id, ref)
    else:
        raise WordDataError(f"型が文字列でもリストでもありません: {row}")

def __AppendWord_str(s: str, book_alias: str, book_id: str, ref: list):
    if len(s.strip()) == 0:
        raise WordDataError(f"空の文字列です ({book_alias}[{'/'.join(ref)}])")
    word = Word(ToHiragana(s), s, None, ref, None, book_alias, book_id)
    TmpFiles.write(word)

def __AppendWord_list(l: list, book_alias: str, book_id: str, ref: list):
    n = len(l)
    if n == 0:
        raise WordDataError(f"空のリストです ({book_alias}[{'/'.join(ref)}])")
    comp, disp = DefParts(l[0])
    if n >= 3:
        desc = l[2]
        if type(desc) == str:
            desc = [desc]
        elif type(desc) != list:
            raise WordDataError(f"説明文(第3の要素)の型が文字列でもリストでもありません: {str(desc)}")
    else:
        desc = None
    word = Word(comp, disp, None, ref, desc, book_alias, book_id)
    TmpFiles.write(word)
    if n >= 2:
        try:
            __AppendAliases(disp, l[1], book_alias, book_id, ref)
        except WordDataError as e:
            Log(e)

# 索引語(あるいはエイリアス)の定義部分(比較用文字列と表示用文字列)を返す
def DefParts(d):
    if type(d) == str:
        return ToHiragana(d), d
    elif type(d) == list:
        if len(d) == 0:
            raise WordDataError("索引語の定義が空のリストです")
        disp = d[0].strip()
        comp = (ToHiragana(disp) if len(d) == 1 else d[1]).strip()
        if disp == '':
            raise WordDataError(f"空の索引語が渡されました: [{repr(disp)}, {repr(comp)}]")
        elif comp == '':
            raise WordDataError(f"空のふりがなが渡されました: [{repr(disp)}, {repr(comp)}]")
        return comp, disp
    else:
        raise WordDataError(f"型が文字列でもリストでもありません: {str(d)} {type(d)}")

def __AppendAliases(orig_disp, aliases, book_alias: str, book_id: str, ref: list):
    if type(aliases) == str:
        aliases = [aliases]
    elif type(aliases) != list:
        raise WordDataError(f"エイリアスの型が文字列でもリストでもありません: {aliases}")
    for alias in aliases:
        try:
            comp, disp = DefParts(alias)
            word = Word(comp, disp, orig_disp, ref, None, book_alias, book_id)
            TmpFiles.write(word)
        except WordDataError as e:
            Log(f"エイリアス {alias} でのエラー {str(e)}")

