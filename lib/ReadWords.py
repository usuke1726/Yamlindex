
from lib.Word import Word
from lib.Book import Book
from lib.Log import Log
from lib.Hiragana import ToHiragana
from lib.ReadDict import DefParts, WordDataError
from lib.TmpFiles import TmpFiles

def __ReadWord(word: dict):
    __ValidateWordFormat(word)
    body = word["body"]
    comp, disp = DefParts(body[0])
    books = [ref for ref in [__RefToBookInfo(ref) for ref in word["ref"]] if not ref is None]
    if len(books) == 0:
        raise WordDataError("有効な文献が指定されていません")
    for book in books:
        word = Word(comp, disp, None, book["ref"], book["desc"], book["alias"], book["id"])
        TmpFiles.write(word)
    if len(body) >= 2:
        try:
            __ReadWord_Alias(disp, body[1])
        except WordDataError as e:
            Log(e)

def __ReadWord_Alias(orig_disp, aliases):
    if type(aliases) == str:
        aliases = [aliases]
    elif type(aliases) != list:
        raise WordDataError(f"エイリアスの型が文字列でもリストでもありません: {aliases} {type(aliases)}")
    for alias in aliases:
        try:
            comp, disp = DefParts(alias)
            word = Word(comp, disp, orig_disp, None, None, None, None)
            TmpFiles.write(word)
        except WordDataError as e:
            Log(f"エイリアス {alias} でのエラー {str(e)}")

def __ValidateWordFormat(word: dict):
    if type(word) != dict:
        raise WordDataError(f"索引語は辞書形式で渡す必要があります {word}")
    if not "body" in word:
        raise WordDataError(f"body プロパティが指定されていません: {word}")
    if not "ref" in word:
        raise WordDataError(f"ref プロパティが指定されていません: {word}")
    for key in {"body", "ref"}:
        if type(word[key]) == str:
            word[key] = [word[key]]
        elif type(word[key]) != list:
            raise WordDataError(f"{key}プロパティの型が文字列でもリストでもありません({type(word[key])}): {word}")
    if len(word["body"]) == 0:
        raise WordDataError(f"bodyプロパティが空のリストです: {word}")

def __RefToBookInfo(ref):
    desc = None
    book_ref = None
    if type(ref) == str:
        book = Book.FromID(ref)
    elif type(ref) == list:
        if len(ref) >= 2:
            book = Book.FromID(ref[0])
            book_ref = ref[1]
            if type(book_ref) == list:
                if len(book_ref) > 0:
                    book_ref = [str(r) for r in book_ref]
                else:
                    book_ref = None
            elif not book_ref is None:
                book_ref = [str(book_ref)]
            if len(ref) >= 3:
                desc = ref[2]
                if type(desc) == list:
                    if len(desc) > 0:
                        desc = [str(d) for d in desc]
                    else:
                        desc = None
                elif not desc is None:
                    desc = [str(desc)]
        elif len(ref) == 1:
            book = Book.FromID(ref[0])
        else:
            return None
    if book is None:
        return None
    else:
        return {"id": book.id, "alias": book.alias, "ref": book_ref, "desc": desc}

def ReadWords(data: dict) -> bool:
    word_added = False
    if not "words" in data:
        raise WordDataError("words プロパティは必須です")
    words = data["words"]
    if type(words) == dict:
        words = [words]
    if type(words) == list:
        for word in words:
            try:
                __ReadWord(word)
                word_added = True
            except WordDataError as e:
                Log(f"データエラー\n{e}\n")
    else:
        raise WordDataError("words プロパティの値は辞書あるいは辞書の配列でなければいけません")
    return word_added

