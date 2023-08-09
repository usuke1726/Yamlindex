
from enum import Enum, auto

class BookType(Enum):
    note = auto()
    paper = auto()
    slide = auto()
    book = auto()
    website = auto()
    other = auto()
    default = other
    @staticmethod
    def from_str(s: str, force: bool = True):
        if s is None:
            return BookType.default
        s = str(s).lower()
        types_map = {
            BookType.note: {'note', 'notes', 'ノート'},
            BookType.paper: {'paper', 'papers', '論文'},
            BookType.slide: {'slide', 'slides', 'スライド'},
            BookType.book: {'book', 'books', '書籍', '本'},
            BookType.website: {'website', 'websites', 'web', 'site', 'sites', 'webサイト'},
            BookType.other: {'other', 'others', 'その他'}
        }
        for k, v in types_map.items():
            if s in v:
                return k
        if force:
            return BookType.default
        else:
            return None
    @staticmethod
    def available_types():
        return BookType.__members__.keys() - ['default']
    @staticmethod
    def is_available(s):
        return not BookType.from_str(s, force = False) is None
    def __eq__(self, s):
        if type(s) == str:
            return self.name == BookType.from_str(s).name
        elif isinstance(s, BookType):
            return self.name == s.name
        else:
            return False
    def __hash__(self):
        return hash(self.name)


