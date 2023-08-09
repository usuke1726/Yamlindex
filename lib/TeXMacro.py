
# HTMLのKaTeX用のマクロを読み込む
import json
import re
# import yaml
import codecs
from os import path
from lib.Log import Log

__HTML_DefaultTeXMacros = {
}
HTML_DefaultTeXMacros_forHelp = "\n".join([f'    {k}: {v}' for k, v in __HTML_DefaultTeXMacros.items()]) if len(__HTML_DefaultTeXMacros) > 0 else "(マクロなし)"
__HTML_TeXMacros = __HTML_DefaultTeXMacros.copy()

def HTML_TeXMacros(as_str: bool = True):
    if as_str:
        return json.dumps(__HTML_TeXMacros)
    else:
        return __HTML_TeXMacros.copy()

class ReadMacroError(Exception):
    pass

def __ValidateDict(data: dict):
    for k, v in data.items():
        if type(k) != str:
            raise ReadMacroError(f"文字列ではありません: {k} {type(k)}")
        elif type(v) != str:
            raise ReadMacroError(f"文字列ではありません: {v} {type(v)}")
        elif not k.startswith("\\"):
            raise ReadMacroError(f"マクロは \\ で始まらないといけません: {k}")

# YAMLファイルだと他の索引ファイルと混同する恐れがあるのでJSONのみとした
# def __ReadMacro_FromYaml(filename: str):
#     with codecs.open(filename, 'r', 'utf-8') as f:
#         data = yaml.safe_load(f)
#     __ValidateDict(data)
#     global __HTML_TeXMacros
#     __HTML_TeXMacros = data

def __ReadMacro_FromJson(filename: str):
    with codecs.open(filename, 'r', 'utf-8') as f:
        data = f.read()
    data = re.sub(r"/\*[\s\S]*?\*/|//.*", "", data)
    data = json.loads(data)
    __ValidateDict(data)
    global __HTML_TeXMacros
    __HTML_TeXMacros = data

def ReadMacro(filename: str):
    try:
        Log(f"TeXマクロ: {filename}")
        p = path.abspath(filename)
        if not path.isfile(p):
            raise ReadMacroError(f"ファイル {p} が見つかりません")
        ext = path.splitext(p)[-1]
        # if ext in {".yaml", ".yml"}:
            # __ReadMacro_FromYaml(p)
        if ext in {".json", ".jsonc"}:
            __ReadMacro_FromJson(p)
        else:
            raise ReadMacroError(f"無効な拡張子です: {ext}")
    except ReadMacroError as e:
        Log(f"TeXマクロ読み込みエラー\n{e}\nデフォルトのマクロ設定を使います\n")

