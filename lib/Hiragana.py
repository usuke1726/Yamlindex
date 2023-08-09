
import pykakasi
import re

__convert = pykakasi.kakasi().convert

# 文字列に漢字やカタカナが含まれていたら全部ひらがなに変換する
def ToHiragana(s: str):
    # 英単語や記号が混ざってもOK
    # 英数字や記号のみでもOK
    s = __EscapeSymbols_BeforeToHiragana(s)
    s = "".join([s['hira'] for s in __convert(s)])
    s = __EscapeSymbols(s)
    return s

# ASCII文字やひらがな以外の記号などを変換(ソートの際にASCII文字の記号と同類として扱わせる)
def __EscapeSymbols(s: str):
    # ドル記号は数式記号のため置き換えない
    # それ以外の記号はみな "/" にまとめる(大小関係は気にしない)
    # ひらがなは ぁ(\u3041) から ゖ(\u3096) までを対象
    pattern = r"[^\$0-9A-Za-z\u3041-\u3096]"
    after = "/" # \u002F, '0'の直前の文字
    return re.sub(pattern, after, s)

# pykakasiでconvertする際に絵文字などが空文字列になる現象があったので，その対策としてあらかじめエスケープする
def __EscapeSymbols_BeforeToHiragana(s: str):
    def escape_onechar(c):
        # 半角/全角スペースは空文字列にならない
        if __convert(c)[0]['hira'] == "":
            return "/" # 記号扱い
        else:
            return c
    return "".join([escape_onechar(c) for c in s])

# [s['hira'] for s in __convert(s) if s['hira'] != ''] ではうまくいかない．1文字ずつ確認する必要がある． (実際に "あ😊い" などで確かめてみると分かる)
