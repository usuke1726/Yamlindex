
import heapq
from lib.TmpFiles import TmpFiles
from lib.Log import Log, Progress
from lib.Word import Word

def MakeSortedFile():
    TmpFiles.flush()
    tmpfiles = TmpFiles.file_pathes
    filenum = len(tmpfiles)
    length = 0
    if filenum == 0:
        return None, 0
    # 分割して書き込んだファイルをそれぞれソート
    with Progress(filenum, "各ファイルをソート") as prog:
        for i in range(len(tmpfiles)):
            logtitle = f"一時ファイル{i+1}"
            path = tmpfiles[i]
            with open(path, 'r') as f:
                lines = f.readlines()
            length += len(lines)
            lines.sort()
            with open(path, 'w') as f:
                f.writelines(lines)
            Log("ソート完了", title = logtitle)
            prog.step()
    # ソートされたファイルをマージする
    with Progress(length, "マージ") as prog:
        try:
            Log("マージ開始")
            # ファイルをいくつか開けるのでwith構文は使えない
            files = [open(f, 'r') for f in tmpfiles]
            output_path = TmpFiles.create_newfile_path()
            output = open(output_path, 'w')
            prev = None
            final_linenum = 0
            for row in heapq.merge(*files):
                if prev is None:
                    prev = Word.from_str(row)
                else:
                    word = Word.from_str(row)
                    if prev == word:
                        # 「同じ」索引語は1つにまとめる
                        prev = prev + word
                    else:
                        # 「違う」ものが現れたら前の索引語を出力する
                        output.write(str(prev) + "\n")
                        prev = word
                        final_linenum += 1
                prog.step()
            output.write(str(prev))
            Log("マージ完了")
        finally:
            output.close()
            for f in files:
                f.close()
    return output_path, final_linenum
