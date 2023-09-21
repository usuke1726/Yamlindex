
import json

from lib.Escape import Escape
from lib.Lang import DEFAULT_LANG
from lib.Format import WordFormat

class Word:
    def __init__(self, comp: str, disp: str, alias: str, ref: list, desc: list, book_alias: str, book_id: str):
        self.compare_word = comp.upper().strip()
        self.display_word = disp.strip()
        if alias is None:
            self.aliases = None
        else:
            self.aliases = [alias]
        if ref is None:
            self.ref = [None]
        else:
            self.ref = [ref.copy()]
        if desc is None:
            self.description = None
        else:
            self.description = [json.dumps({
                'desc': str(d),
                'book_alias': book_alias,
                'ref': ref
            }) for d in desc]
        self.book_aliases = [book_alias]
        if book_id is None:
            self.book_ids = []
        else:
            self.book_ids = [book_id]
    def head(self):
        return self.compare_word[0]
    def __str__(self):
        data = {
            # Python version>=3.7のdict型はキーの順序を保存する
            # -> 比較用文字列 comp が必ず先頭になる
            # -> 単純な文字列の比較で索引語をソートできる
            'comp': self.compare_word,
            'is_not_alias': self.aliases is None, # ailasとそうでないものとでソートしたときにまとまるようにする(これがないと索引語の結合がうまくいかない)
            'disp': self.display_word,
            'aliases': self.aliases,
            'ref': self.ref,
            'description': self.description,
            'book_aliases': self.book_aliases,
            'book_ids': self.book_ids
        }
        return json.dumps(data, ensure_ascii = True, sort_keys = False, separators = (',', ':'))
    @staticmethod
    def from_str(s: str):
        data = json.loads(s)
        word = Word(data['comp'], data['disp'], None, None, None, None, None)
        for key in {'aliases', 'ref', 'book_aliases', 'book_ids', 'description'}:
            setattr(word, key, data[key])
        return word
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
        def escape_description(desc):
            if desc is None:
                return None
            return [
                {
                    'desc': e(d['desc'], onlyInlineMath = False),
                    'book_alias': e(d['book_alias']),
                    'ref': e(d['ref'])
                }
                for d in [json.loads(d) for d in desc]
            ]
        class Info:
            def __init__(self, disp, aliases, book_aliases, book_ids, ref, desc):
                self.disp = disp
                self.aliases = aliases
                self.book_aliases = book_aliases
                self.book_ids = book_ids
                self.ref = ref
                self.desc = desc
        info = Info(
            e(self.display_word),
            e(self.aliases),
            e(self.book_aliases),
            e(self.book_ids),
            e(self.ref),
            escape_description(self.description)
        )
        return WordFormat(lang)(info)
    def __eq__(self, other):
        same_comp = self.compare_word == other.compare_word
        same_disp = self.display_word == other.display_word
        both_are_alias_or_not = (self.aliases is None) == (other.aliases is None)
        return same_comp and same_disp and both_are_alias_or_not
    def __ne__(self, other):
        return not (self == other)
    def copy(self):
        return Word.from_str(str(self))
    def __add__(self, other):
        if self.aliases is None:
            if not other.aliases is None:
                self.aliases = other.aliases.copy()
        elif not other.aliases is None:
            self.aliases = list(set(self.aliases).union(set(other.aliases)))
        self.ref.extend(other.ref)
        self.book_aliases.extend(other.book_aliases)
        self.book_ids.extend(other.book_ids)
        if self.description is None:
            if not other.description is None:
                self.description = other.description.copy()
        elif not other.description is None:
            self.description.extend(other.description)
        return self.copy()

