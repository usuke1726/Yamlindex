
from functools import partial
from tqdm import tqdm as std_tqdm
# ターミナル幅の変更による表示崩れを防止
tqdm = partial(std_tqdm, dynamic_ncols = True)
from contextlib import contextmanager
import time
from sys import stderr # プログレスバーやログ出力は常に標準エラー出力

# tqdmのWrapper的なオブジェクト
class ProgressManager:
    __PROGLEVEL = 0
    __Progresses = [None, None, None]
    def __init__(self, count: int, desc: str = ""):
        self.__opened = True
        ProgressManager.__PROGLEVEL += 1
        level = ProgressManager.__PROGLEVEL
        self.__level = level
        assert level in [1, 2, 3]
        assert count >= 1
        # 一番上のプログレスバーのpos属性を0にして，その上のバーはpos = -1となるようにする
        self.__pbar = tqdm(total = count, position = -1, desc = desc, leave = False, file = stderr)
        ProgressManager.__Progresses[level - 1] = self.__pbar
        for i in range(level):
            ProgressManager.__Progresses[i].pos -= 1
    def __del__(self):
        self.close()
    def step(self):
        if self.__opened:
            f = self.__pbar.update(1)
    def close(self):
        if self.__opened:
            # 子プログレスも先に終了することはないと想定
            assert self.__level == ProgressManager.__PROGLEVEL
            self.__pbar.close()
            ProgressManager.__Progresses[ProgressManager.__PROGLEVEL-1] = None
            ProgressManager.__PROGLEVEL -= 1
            for i in range(ProgressManager.__PROGLEVEL):
                ProgressManager.__Progresses[i].pos += 1
            self.__opened = False

@contextmanager
def Progress(count: int, desc: str = ""):
    progress = ProgressManager(count, desc)
    try:
        yield progress
    finally:
        progress.close()

def Log(*args, title: str = ""):
    if title.strip() == '':
        head = ""
    else:
        head = f"{title}: "
    s = " ".join([str(arg) for arg in args])
    tqdm.func.write(head + s, file = stderr)

