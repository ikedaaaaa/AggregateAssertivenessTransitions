# AggregateAssertivenessTransitions
アサーティブな会話をしている箇所，していない箇所のアンケートデータを集計するプログラム

活性度評価のデータとほぼ同じプログラムになる気がしている．集計する形式が同じになりそう．
## 1. コンテナを作成する．
``` bash
# yml,dockerfile,requirements.txtを編集した場合はbuildをする必要がある
docker compose -f compose.yml up --build -d

# buildをしなくてもいい場合
docker compose -f compose.yml up  -d
```

## 2. コンテナ内に入る．
``` bash
docker exec -it AggregateAssertivenessTransitions bash   
```

## 3. コンテナ内でpythonファイルを実行する
``` bash
# python main.py {集計するディレクトリ}
例：python main.py 実験後データ
```

## 4. コンテナを壊す
``` bash
docker compose -f compose.yml down  
```

# 開発中の注意点
## 新しいパッケージを入れたい場合
```bash
# コンテナ内で実行
pip install {package}

# 次にコンテナを立てるときにそのパッケージを入れることができるために実行
pip freeze > requirements.txt
```

# プログラムの仕様
## ディレクトリ構造
```
実験_アサーティブの遷移/
    ┝ 02実験後データ/
        ┝ 実験_アサーティブの遷移_{数字}_{名前}/
        │    └ {数字}/
        │    │     └ {数字}_conv_file/
        │    │     │   └ {数字}_00.wav
        │    │     │   └ {数字}_01.wav
        │    │     │   ...
        │    │     └ assertiveness_transitions_{数字}_first_data.csv
        │    │     └ assertiveness_transitions_{数字}_second_data.csv
        │    │     └ target_conversation_degree_{数字}_first_data.csv
        │    │     └ target_conversation_degree_{数字}_second_data.csv
        │    └ {数字}/
        │    └ アサーティブな会話とは.pdf
        │    ...
        ┝ 実験_活性度調査_{数字}_{名前}/
        ┝ 実験_活性度調査_{数字}_{名前}/
        ┝ 実験_活性度調査_{数字}_{名前}/
```

## ファイルの中身
```
assertiveness_transitions_{数字}_first_data.csv
cid,sid,assertiveness
00_00,00_00.wav,1
00_01,00_01.wav,2
...
00_30,00_30.wav,3

target_conversation_degree_{数字}_first_data.csv
conv_name,TargetConversationDegree
{数字}_first,3
```

## したいこと
全ての区間でその区間がアサーティブな会話をしているか，していないかを集計したい．

各区間のアサーティブ度合いを集計して，負の値になっている区間を見つけたい．（アサーティブな会話をしていない区間を見つけたい）

それは実験参加者の平均で求める

また，各会話（15分）が，目標としたい会話であるか，そうでないかを集計し，アサーティブ点という指標が妥当であったかを検証したい．

なお，assertiveness_transitions_{数字}_first_data.csvは[1,2,3,4,5,6,7] = [非常にアサーティブな会話をしていない，かなりアサーティブな会話をしていない，少しアサーティブな会話をしていない，どちらでもない，少しアサーティブな会話をしている，かなりアサーティブな会話をしている，非常にアサーティブな会話をしている]
target_conversation_degree_{数字}_first_data.csvは[1,2,3,4,5,6,7] = [非常に目標としたい会話ではない，かなり目標としたい会話ではない，少し目標としたい会話ではない，どちらでもない，少し目標としたい会話である，かなり目標としたい会話である，非常に目標としたい会話である]

## プログラムの簡単な手順
### 1.データを読み込む
#### 1.1.アサーティブ度合いのデータを読み込む
実験参加者それぞれのアサーティブ度合いのデータを読み込む（実験参加者それぞれの「assertiveness_transitions_{数字}_first_data.csv，assertiveness_transitions_{数字}_second_data.csv」）

実験参加者のリストを作成(personal_assertiveness_transitions_list)．その中身は[column=cid,assertiveness]のデータフレーム

```
ex)
personal_assertiveness_transitions_list[0]
cid,assertiveness
00_00,5.0
00_01,3.0
...
14_59,5.0

personal_assertiveness_transitions_list[1]
cid,assertiveness
00_00,3.0
00_01,1.0
...
14_59,3.0
```

#### 1.2.目標としたい会話であるかどうかの評価のデータを読み込む
実験参加者それぞれの目標としたい会話であるかどうかの評価のデータを読み込む（実験参加者それぞれの「target_conversation_degree_{数字}_first_data.csv，target_conversation_degree_{数字}_second_data.csv」）

実験参加者のリストを作成(personal_target_conversation_degree_list)．その中身は[column=conv_name,TargetConversationDegree]のデータフレーム

```
personal_target_conversation_degree_list[0]
conv_name,TargetConversationDegree
00_first,3
00_second,1
01_first,1
...
14_second,0

personal_target_conversation_degree_list[1]
conv_name,TargetConversationDegree
00_first,2
00_second,1
01_first,1
...
14_second,1
```

### 2.アサーティブ度合いを集計する
各実験参加者のcidごとのアサーティブ度合いを集計する．

cidごとのアサーティブ度合いの平均値を出す．その結果を「assertiveness_transitions_average_df」に格納

```
assertiveness_transitions_average_df
cid,AverageAssertiveness
00_00,3.0
00_01,0.2
...
14_59,2.2
```

### 3.アサーティブ度合いが負の値であるものを抽出する
assertiveness_transitions_average_dfのなかで，assertivenessが負の値になっているcidを集める．

変数をいじってcidを集める閾値を変更できるようにしてほしい．（assertivenessが-1以下のcidを集めるなど）

その結果を「unassertiveness_conv_df」に格納する

```
unassertiveness_conv_df
cid,AverageAssertiveness
10_34,2.0
12_06,0.2
...
13_29,2.6
```

### 4.目標としたい会話であるかどうかの評価を集計する
各実験参加者の目標としたい会話であるかどうかの評価を集計する．

conv_nameごとの評価値の平均値を出す．その結果を「target_conversation_degree_average_df」に格納する

```
target_conversation_degree_average_df
conv_name,AverageTargetConversationDegree
00_first,2.2
00_second,0.4
01_first,2.0
...
14_second,2.1
```

### 5.並べる
target_conversation_degree_average_dfを，AverageTargetConversationDegreeの値順にソートする（target_conversation_degree_average_dfを直接変更）．

### 6.出力する
unassertiveness_conv_dfとtarget_conversation_degree_average_dfをcsvに出力する．
それぞれ「unassertiveness_conv.csv，target_conversation_degree_average.csv」というファイル名で保存する
