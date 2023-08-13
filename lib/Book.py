
from lib.Escape import Escape
from lib.Lang import DEFAULT_LANG
from lib.Format import BookFormat
from lib.BookType import BookType

class BookHeaderError(Exception):
    pass

# 論文・書籍等の文献データ
class Book:
    __Types = {"note", "paper", "slide", "book", "other"}
    __Keys = {"type", "title", "related", "alias", "description", "year", "author", "publisher", "ISBN", "DOI", "URL", "last_accessed", "path"}
    __Keys_Required = {"title", "alias"}

    def __init__(self, header: dict):
        Book.__Assert_Includes_AllKeysRequired(header)
        Book.__Assert_NotIncludes_OtherProperties(header)
        for key in Book.__Keys:
            setattr(self, key, None)
        for key, val in header.items():
            if type(val) == list:
                v = [str(v) for v in val]
            else:
                v = str(val)
            setattr(self, key, v)
        if not self.year is None and self.year.lower() in {"unknown", "不明"}:
            self.year = "作成年不明"
        if not self.author is None and self.author.lower() in {"unknown", "不明"}:
            self.author = "著者不明"
        self.__validate_valuetypes()
        Book.__Assert_IsValidType(self.type)
        self.type = BookType.from_str(self.type)
    def __str__(self):
        return self.format()
    def format(self, lang: str = DEFAULT_LANG):
        escape = Escape(lang)
        def e(v, onlyInlineMath: bool = True):
            if v is None:
                return None
            elif type(v) == str:
                return escape(v, onlyInlineMath = onlyInlineMath)
            elif type(v) == list:
                return [e(a, onlyInlineMath = onlyInlineMath) for a in v]
            else:
                return None
        keys = Book.__Keys
        class Info:
            def __init__(self, book):
                for k in keys:
                    setattr(self, k, e(getattr(book, k), onlyInlineMath = (k != 'description')))
                self.URL = book.URL
                self.type = book.type
        info = Info(self)
        return BookFormat(lang)(info)
    def __validate_valuetypes(self):
        keys_withTypeList = {"description", "related"}
        for key in Book.__Keys:
            val = getattr(self, key)
            if val is None:
                continue
            elif key in keys_withTypeList:
                if type(val) == str:
                    continue
                elif type(val) == list:
                    for s in val:
                        if type(s) != str:
                            raise BookHeaderError(f"リスト {val} の中に文字列でない型の値があります: {s}")
                else:
                    raise BookHeaderError(f"{key} の型が文字列でも配列でもありません: {val}")
            elif type(val) != str:
                raise BookHeaderError(f"{key} の型が文字列ではありません: {val})")
    @staticmethod
    def __Assert_Includes_AllKeysRequired(header: dict):
        notinclude = {key for key in Book.__Keys_Required if not key in header}
        if len(notinclude) > 0:
            raise BookHeaderError("\n".join([f"必須パラメータ {key} が未指定です" for key in notinclude]))
    @staticmethod
    def __Assert_NotIncludes_OtherProperties(header: dict):
        include = {key for key in header if not key in Book.__Keys}
        if len(include) > 0:
            raise BookHeaderError("\n".join([f"ヘッダーに想定しないパラメータ {key} が含まれています" for key in include]))
    @staticmethod
    def __Assert_IsValidType(tp: str):
        if not BookType.is_available(tp):
            raise BookHeaderError(f"想定しないタイプです: {tp}\n次のいずれかにしてください: {', '.join(BookType.available_types())}")
    # Yamlファイルから得たデータからヘッダーを抽出する(ついでにヘッダー情報をデータから消去する)
    @staticmethod
    def ExtractHeader_FromDict(data: dict):
        # プロパティは大文字小文字を区別する
        # dataは参照渡しなので中身が変更される
        out = {}
        for key in Book.__Keys:
            if key in data:
                out[key] = data[key]
                del data[key]
        return out



