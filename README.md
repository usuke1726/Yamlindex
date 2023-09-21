
# Yamlindex

特定のフォーマットに従った索引語(Yamlファイル)を統合し，五十音順に並び替えするツールです．

出力ファイルの形式は，現在 **HTML, Markdown** をサポートしています．(推奨はHTML．)

## コマンドラインオプション

- `-h`, `--help`: ヘルプ文を出力
- `-v`, `--version`: バージョンを出力
- `-d`, `--dir`: Yamlファイルがあるフォルダ(複数指定可，ファイル指定可)
    - デフォルト: `.`
- `-o`, `--output`: 出力ファイルのパス(拡張子も含む)
    - デフォルト: `./out.(デフォルト拡張子)`
- `-r`, `--recurse`: `--dir`で与えたディレクトリから再帰的にYamlファイルを探索
- `-f`, `--force`: 出力ファイルが既存でも確認しない，`-o`オプション未指定の場合にデフォルトファイルを設定する，など
- `x`, `--exclude`: 除外するYamlファイルのパス(複数指定可)
- `--macro`: TeXのマクロを指定したJsonファイルのパス(現在HTML専用)
- `--stdout`: 出力をファイル出力ではなく標準出力として行う
- `-l`, `--lang`: 出力言語を設定(`-o`オプションで拡張子として指定したものより優先度が高い)
- `--hiragana`, `--hurigana`, `--ruby`: 文字列を与えるとそのふりがなを出力する

## 注意点

- Yamlファイルの文字コードは必ず **UTF-8** にしてください！BOMはあってもなくても構いません．また，改行コードはLFでもCRLFでも大丈夫のようです．
- 基本的に数式 `$ ... $` を利用可能ですが，`description`以外ではブロック数式 `$$ ... $$`，`\[ ... \]` はインライン数式に置き換えられます．
- Yamlの言語仕様に注意してください．
    - 0から始まり，8や9を含まない数値は **8進数の数値** として扱われます．
    - 次の文字列は **異なる型** (bool型やnullオブジェクト)として扱われるので，意図した表示にならない可能性があります．以下の文字列を与える場合はクォーテーションで囲むようにしましょう．
        - y, Y, yes, Yes, YES
        - n, N, no, No, NO
        - true, True, TRUE
        - false, False, FALSE
        - on, On, ON
        - off, Off, OFF
        - null, Null
    - 索引語ファイルは，ハイライト機能を持つテキストエディタでの作成をおススメします！


## 索引語データの書き方

### ヘッダー

ヘッダーには書籍情報を記述します．
なお，下記パラメータ以外はすべて索引語コンテンツとみなされます．

*印は必須パラメータ

|名前|型|概要|
|:-:|:-:|:-:|
|*`title`|`str`|タイトル|
|`alias`|`str`|別名<br>(各単語において表示)<br>(重複可能)|
|`id`|`str`|文献ID<br>(半角英数字，ハイフン，<br>アンダーバーのみ．)<br>(重複禁止)|
|`type`|`str`|文献の種類<br>(`note`\|`paper`\|`slide`\|`book`\|<br>`website`\|`word`\|`other`)<br>(別名あり)|
|`author`|`str`|著者・作成者|
|`year`|`str`\|`int`|発表年・作成年|
|`description`|`str`\|`list[str]`|説明文(自由記述)|
|`related`|`str`\|`list[str]`|関連書籍・関連情報など|
|`publisher`|`str`|出版社
|`ISBN`|`str`|書籍のISBN|
|`DOI`|`str`|文献のDOI|
|`URL`|`str`|URL|
|`last_accessed`|`str`\|`int`|最終アクセス日時|
|`path`|`str`\|`list[str]`|ファイルパス|

#### 文献タイプの別名

- `note`: `notes`, `ノート`
- `paper`: `papers`, `論文`
- `slide`: `slides`, `スライド`
- `book`: `books`, `書籍`, `本`
- `website`: `websites`, `web`, `site`, `sites`, `webサイト`
- `word`: `words`
- `other`: `others`, `その他`

なお，タイプ名は大文字小文字の区別はありません．
また，`word`タイプは，異なる文献の索引語を列挙する特殊な書式として扱われます．詳しくは後述．

### 索引語

基本フォーマットは以下の通りです．

`- [[索引語, ふりがな], [[エイリアス1, ふりがな], [エイリアス2, ふりがな], ...], [説明文1, 説明文2, ...]]`

上記の通り，「**索引語の定義，エイリアスのリスト，説明文のリストの3要素**」から構成されます．

ただし，エイリアスのリストと説明文のリストは**省略可能**です．

- \[第1要素\] 索引語の定義:
    - **ふりがなを指定しない**場合は，`索引語`と角括弧を省略することができます．
    - その場合，ふりがなが自動で振られますが，意図したふりがなでない可能性があります．
        - どのようにふりがなが振られるかは，`--hiragana` あるいは `--hurigana` オプションを用いて確認できます．
- \[第2要素\] エイリアスのリスト
    - 索引語にエイリアスを指定することができます．
        - 英訳や呼び方が複数通りある場合などに有用です．
    - エイリアスも本体の索引語と同様，**ふりがなを指定しない**ことができます．(その場合は角括弧を省略可能です．)
- \[第3要素\] 説明文のリスト
    - 説明文を指定します．ここでは，**ブロック数式**を用いることができます．
    - 説明文が1つのみの場合は，角括弧を省略することができます．

#### 省略の例

`- [[元, げん], [[要素, ようそ], [element, element]], [説明文]]` (オリジナルの書き方)

↓

`- [[元, げん], [[要素, ようそ], element], 説明文]` (不要なリスト表記を省略)

↓

`- [[元, げん], [要素, element], 説明文]` (「要素」はふりがなの間違えようがないとしてふりがなを省略)

↓

`- [[元, げん], [要素, element]]` (特に説明することがないので説明文を省略)

↓

`- [[元, げん]]` (エイリアスも不要として削除．なお，このとき**2重括弧**でないと「げん」がエイリアス扱いになってしまうので注意．)

↓

`- 元` (やっぱり「元」もふりがな不要と判断．このとき角括弧はすべて省略できる．)

### 見出しの階層化

第1章/第1節/第1項 のように見出しを階層化することができます．

階層化は次のように記述します．

```yaml
第1章:
    第1節: # 見出し語のみのリストはハイフン不要
        - 序論に出てきた単語
        - 第1項: # 索引語と見出し語が混ざると，見出し語の方にもハイフンが必要
            - 単語1
            - 単語2
        - 第2項:
            - 単語3
    第2節:
        - 単語4
第2章:
    - 単語3 # もちろん同じ索引語が別の場所にあってもOK
```

### 数式について

数式を利用することができます．

HTMLではKaTeXを利用します．
さらに，HTMLではマクロを設定することができます．
マクロをJsonファイルで記述し，`--macro` オプションで指定してください．

デフォルトのマクロについてはヘルプを参照ください．

## 文献タイプ`word`の特殊書式

通常の書式は，一つの文献に対してそこに含まれている索引語を列挙する形ですが，`type: word`とすることで，一つの索引語に対して文献を指定する逆引きのような形でデータを与えることができます．

Yamlファイルの例：

```yaml
type: word # wordsでもOK
title: テーマ〇〇について # titleはなくてもOK

words: # 必須プロパティ．wordはNG．
  # 各要素にはbody(索引語の情報)とref(その索引語が書かれてある文献の情報)を指定する(どちらも必須)
  - body: 索引語1 # bodyに索引語を指定(通常と同じ書式)
    ref: 文献1のID # 索引語1が書かれている文献(別のYamlファイルでその文献をID付きで記述する必要がある)
  - body: [索引語2, エイリアス]
    ref:
      # 各文献情報はID，文献内の場所，説明文の順に指定する
      - [文献1のID, [第1章, 第2節], [説明文1, 説明文2]]
      - [文献1のID, [第2章, 第3節], [説明文3]] # 同じ文献があってもOK
      - [文献2のID, [], 説明文] # 第2要素なしで説明文を指定する場合は空のリストを第2要素に空のリストを入れる
  - body: [[索引語3, ふりがな], [[エイリアス1, ふりがな], [エイリアス2, ふりがな]]]
    ref: [[文献3のID, p. 48]] # 1重括弧だと2つの文献と解釈されてしまうので2重括弧である必要がある
```

