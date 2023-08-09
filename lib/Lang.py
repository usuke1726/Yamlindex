
# 出力ファイルの言語

from enum import Enum, auto

class OutputLanguageError(Exception):
    pass

_AVAILABLE_EXT = [".md", ".html"]

class Lang(Enum):
    other = auto()
    md = auto()
    html = auto()
    default = html
    @staticmethod
    def from_str(s: str, raiseError: bool = False):
        if s.startswith('.'):
            s = s[1:]
        s = s.lower()
        if s in {"md", "markdown"}:
            return Lang.md
        elif s in {"html", "htm"}:
            return Lang.html
        else:
            if raiseError:
                raise OutputLanguageError(f"言語 {s} は無効です\n有効な言語: {', '.join(_AVAILABLE_EXT)}")
            else:
                return Lang.other
    @staticmethod
    def is_available_ext(ext: str):
        return Lang.from_str(ext, raiseError = False) != Lang.other
    def __eq__(self, s):
        if type(s) == str:
            return self.name == Lang.from_str(s).name
        elif isinstance(s, Lang):
            return self.name == s.name
        else:
            return False
    def __hash__(self):
        return hash(self.name) # Langインスタンスをキーとする辞書に対して["md"]や["html"]としてもアクセスできる

DEFAULT_LANG = Lang.default.name
