
import tempfile

# Wordデータをファイル分割しながら一時ファイルに退避させるクラス
# 膨大なデータを扱うことも想定してメモリを使いすぎないようにする
class TmpFiles:
    file_pathes = []
    __buffer = []
    __active_file = None
    MAX_LENGTH = 1000
    @staticmethod
    def write(s):
        TmpFiles.__buffer.append(str(s) + "\n") # 末尾には自動で改行が入るので，引数の文字列の末尾には改行を入れない
        if len(TmpFiles.__buffer) >= TmpFiles.MAX_LENGTH:
            TmpFiles.flush()
    @staticmethod
    def flush():
        if len(TmpFiles.__buffer) > 0:
            TmpFiles.__create_newfile()
            TmpFiles.__active_file.writelines(TmpFiles.__buffer)
            TmpFiles.__buffer.clear()
            TmpFiles.__file_close()
    @staticmethod
    def __file_close():
        TmpFiles.__active_file.close()
        TmpFiles.__active_file = None
    @staticmethod
    def __create_newfile():
        path = TmpFiles.create_newfile_path()
        TmpFiles.file_pathes.append(path)
        TmpFiles.__active_file = open(path, "w")
    @staticmethod
    def create_newfile_path():
        return tempfile.mktemp()


