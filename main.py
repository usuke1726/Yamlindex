
import sys
import argparse
import traceback

# __pycache__ が作成されないようにする(パフォーマンスが気になるならコメントアウトしてもよい)
sys.dont_write_bytecode = True

from lib.OutFile import GetOutputFilePath, GetOutputFile, GetExtension
from lib.YamlFileList import GetYamlFiles
from lib.Hiragana import ToHiragana
from lib.ReadDict import ReadDict, WordDataError
from lib.ReadWords import ReadWords
from lib.Log import Log, Progress
from lib.Lang import Lang, DEFAULT_LANG
from lib.Book import Book, BookHeaderError
from lib.Word import Word
from lib.Sort import MakeSortedFile
from lib.YamlToDict import YamlToDictList, YamlLoadError
from lib.TeXMacro import ReadMacro
from lib.Header import PrintTopHeader, PrintBookHeader, PrintFooter, HeadChar
from lib.Help import HELP_DESCRIPTION, HELP_EPILOG, HELP_VERSION

parser = argparse.ArgumentParser(
formatter_class=argparse.RawTextHelpFormatter, # \nや\tを反映させる
description = HELP_DESCRIPTION,
epilog = HELP_EPILOG
)
parser.add_argument('-d', '--dir', nargs = "+", type = str, help = "YAMLファイルが格納されているフォルダのパス\n\tスペース区切りで複数指定可\n\t未指定可(カレントディレクトリになる)\n\tファイルも指定可能(末尾を .yml または .yaml にする)", default = ["."])
parser.add_argument('-x', '--exclude', nargs = "+", type = str, help = "除外するYAMLファイルのパス\n\tスペース区切りで複数指定可\n\t未指定可", default = [])
default_filename = f"./out.{DEFAULT_LANG}"
parser.add_argument('-o', '--output', type = str, help = f"出力ファイルパス\n\t拡張子も含む\n\t未指定可(デフォルトは {default_filename} )", default = default_filename)
parser.add_argument('-r', '--recurse', action = "store_true", help = "--dirで指定したフォルダのサブフォルダからも再帰的にYAMLファイルを探す")
parser.add_argument('-f', '--force', action = "store_true", help = "ファイル作成を強制的に行う\n\toutputが既存でも確認しない\n\toutput未指定でも勝手にファイル名を補完する\n\tなど...")
parser.add_argument('--macro', type = str, help = "(HTML用)TeXのマクロを指定したJSONファイルのパス(未指定可)", default = None)
parser.add_argument('-v', '--version', action = "store_true", help = "バージョンを出力")
parser.add_argument('--stdout', action = "store_true", help = "実行結果をファイル出力ではなく標準出力する")
parser.add_argument('-l', '--lang', type = str, help = "出力ファイルの拡張子を指定する", default = None)

parser.add_argument('--hiragana', '--hurigana', type = str, help = "ひらがなへの変換結果を表示", default = None)

args = parser.parse_args()

# 引数処理
if args.version:
    print(HELP_VERSION)
    exit(0)
elif not args.hiragana is None:
    print(f"{args.hiragana} -> {ToHiragana(args.hiragana)}")
    exit(0)

yamlfiles = GetYamlFiles(args.dir, args.recurse, args.exclude)
Log(f"Yamlファイル: {yamlfiles}")

if not args.macro is None:
    ReadMacro(args.macro)

is_stdout = args.stdout
if not args.lang is None:
    out_ext = Lang.from_str(args.lang, raiseError = True).name
elif is_stdout:
    out_ext = DEFAULT_LANG
else:
    out_ext = GetExtension(args.output)

if is_stdout:
    outfilename = "stdout"
else:
    outfilename = GetOutputFilePath(args.output, args.force)
Log(f"出力ファイル: {outfilename} (言語: {out_ext})")

filenum = len(yamlfiles)
anything_suceeded = False

Log("\n\n======== START ========\n")

# 索引語データを読み込んで一時ファイルに出力
with Progress(filenum, "yamlload") as prog:
    words_buffer = []
    for i in range(filenum):
        try:
            filename = yamlfiles[i]
            Log(f"** Yamlfile ** {filename} {i+1}/{filenum}:")
            data = YamlToDictList(filename)
        except YamlLoadError as e:
            Log(f"Yamlファイルロード失敗 文法に誤りがある可能性があります")
            prog.step()
            continue
        book_num = len(data)
        if book_num == 0:
            Log("文献がありません")
            continue
        with Progress(book_num, "yamlload-onebook") as prog2:
            for d in data:
                try:
                    if "type" in d and d["type"] in {"word", "words"}:
                        words_buffer.append([filename, d])
                        continue
                    header = Book.ExtractHeader_FromDict(d)
                    book = Book(header)
                    ReadDict(d, book.alias, book.id)
                    anything_suceeded = True
                except WordDataError as e:
                    Log(f"Yamlファイル読み込み失敗\n{e}\n")
                except BookHeaderError as e:
                    Log(f"ヘッダーエラー\n{e}")
                except Exception as e:
                    Log(f"エラー\n{e}\n")
                    Log(''.join(traceback.format_tb(e.__traceback__)))
                finally:
                    prog2.step()
        prog.step()
    for words in words_buffer:
        try:
            Log(f"** Words from {words[0]} **")
            result = ReadWords(words[1])
            anything_suceeded = result or anything_suceeded
        except WordDataError as e:
            Log(f"Yamlファイル読み込み失敗\n{e}\n")
        except Exception as e:
            Log(f"エラー\n{e}\n")
            Log(''.join(traceback.format_tb(e.__traceback__)))

if not anything_suceeded:
    Log(f"どのYamlファイルも読み込みに失敗したので終了します")
    exit(1)
# 書き込んだ一時ファイルをソートする
sorted_filename, linenum = MakeSortedFile()

# ソートしたファイルを読み込んでフォーマットして最終ファイルに出力
books = Book.Books()
booknum = len(books)
with Progress(linenum + booknum, "output") as prog, \
     GetOutputFile(outfilename, is_stdout) as outfile:
    PrintTopHeader(outfile, lang = out_ext)
    if linenum > 0:
        with open(sorted_filename, 'r') as sorted_file:
            for row in sorted_file.readlines():
                word = Word.from_str(row)
                HeadChar.apply(outfile, word, out_ext)
                out = word.format(lang = out_ext) + "\n"
                outfile.write(out)
                prog.step()
    else:
        Log("索引語が1つも追加されませんでした\n文献の情報だけを出力します")
    PrintBookHeader(outfile, lang = out_ext)
    for book in books:
        out = book.format(lang = out_ext) + "\n"
        outfile.write(out)
        prog.step()
    PrintFooter(outfile, lang = out_ext)

Log("done\n\033[2K") # 一番下のプログレスバーが残っていることがあるので消去する
