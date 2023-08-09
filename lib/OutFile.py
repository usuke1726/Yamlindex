
import io
import codecs
from os import path
from sys import stdout, stderr
from lib.Lang import Lang, DEFAULT_LANG
from contextlib import contextmanager
from lib.Log import Log

# 出力ファイル名の存在チェックをした上で，絶対パスを返す
def GetOutputFilePath(p: str, force: bool):
    if p is None or p.strip() == '':
        if force:
            p = f"./out.{DEFAULT_LANG}"
        else:
            Log("出力パスを指定してください")
            exit(2)
    if path.isdir(p):
        if force:
            p = f"{p}/out.{DEFAULT_LANG}"
        else:
            Log(f"{p} は存在するディレクトリです\nファイルパスを指定してください")
            exit(2)
    abspath = path.abspath(p)
    if path.isfile(p) and (not force):
        s = input(f"{p} は既に存在しているようですが，上書きしますか？ (Y/N) > ").lower()
        if s == 'n':
            Log("終了します")
            exit(0)
    return abspath

def GetExtension(p: str):
    ext = path.splitext(p)[-1]
    return Lang.from_str(ext, raiseError = True).name

# stdoutへの出力も想定したファイル取得関数
@contextmanager
def GetOutputFile(path: str, is_stdout: bool):
    if is_stdout:
        # (PowerShell/コマンドプロンプト)出力結果を変数に格納したりパイプに渡そうとすると yield stdout ではエラーが生じる
        # これは HTML出力ヘッダに含まれる ▶(\u25b6) がCP932文字でないことが原因であり，stdoutのエンコードをutf-8にする必要がある
        # (上の記号を使わなくともユーザからの入力データ次第で同様の現象が起こりうるので，上記の対応は必要)
        # なお，この設定によって文字化けを起こす可能性があるが，これはシェルの方で対応可能: PowerShellなら [console]::OutputEncoding = [System.Text.UTF8Encoding]::new() を先に実行しておけば問題ない
        yield io.TextIOWrapper(stdout.buffer, encoding='utf-8')
    else:
        f = codecs.open(path, 'w', 'utf-8')
        try:
            yield f
        finally:
            f.close()
