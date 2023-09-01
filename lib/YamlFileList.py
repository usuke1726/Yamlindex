
from os import path
from glob import glob
from lib.Log import Log

def __GetYamlFiles_FromOneDir(directory: str, recurse: bool):
    if directory.endswith('.yml') or directory.endswith('.yaml'):
        return [path.abspath(f) for f in glob(directory, recursive=True) if path.isfile(f)]
    elif not path.isdir(directory):
        Log(f"ディレクトリ {directory} が見つかりません")
        return []
    if recurse:
        files = glob(path.join(directory, '**/*.yml'), recursive=True) + glob(path.join(directory, '**/*.yaml'), recursive=True)
    else:
        files = glob(path.join(directory, '*.yml')) + glob(path.join(directory, '*.yaml'))
    return [path.abspath(f) for f in files]

def GetYamlFiles(directories: list, recurse: bool, exclude: list):
    files = sum([__GetYamlFiles_FromOneDir(d, recurse) for d in directories], [])
    excluding_files = sum([__GetYamlFiles_FromOneDir(d, recurse) for d in exclude], [])
    out = list(set(files) - set(excluding_files))
    if len(out) == 0:
        Log(f"Yamlファイルが1つも見つからないので終了します")
        exit(2)
    return out

