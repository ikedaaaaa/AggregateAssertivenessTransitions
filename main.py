#!usr/bin/env python
# -*- cording: utf-8 -*-

import sys
import glob
import pandas as pd
import os
from pathlib import Path
import re

def load_csv(base_directory):
    personal_assertiveness_transitions_list = []

    # 各実験フォルダを検索(実験_活性度調査_* にマッチするフォルダをすべて取得)
    experiment_dirs = sorted(glob.glob(os.path.join(base_directory, "*")))

    
    # 各フォルダを順に処理
    for experiment_dir in experiment_dirs:
        # 2桁の数字のフォルダを取得
        sub_dirs = sorted(
            [d for d in glob.glob(os.path.join(experiment_dir, "*")) if re.fullmatch(r"\d{2}", os.path.basename(d))]
        )

        personal_list = []
        for sub_dir in sub_dirs:
            first_data_path = os.path.join(sub_dir, f"assertiveness_transitions_{os.path.basename(sub_dir)}_first_data.csv")
            second_data_path = os.path.join(sub_dir, f"assertiveness_transitions_{os.path.basename(sub_dir)}_second_data.csv")

            if os.path.exists(first_data_path):
                df_first = pd.read_csv(first_data_path, usecols=["cid", "assertiveness"])
                personal_list.append(df_first) #ファーストデータを追加する


            if os.path.exists(second_data_path):
                df_second = pd.read_csv(second_data_path, usecols=["cid", "assertiveness"])
                personal_list.append(df_second) #セカンドデータを追加する
        


        result_df = pd.concat(personal_list,ignore_index=True)
        personal_assertiveness_transitions_list.append(result_df)

    return personal_assertiveness_transitions_list

def calc(personal_assertiveness_transitions_list):

    # すべてのデータフレームを結合
    df_all = pd.concat(personal_assertiveness_transitions_list)

    # cidごとのassertivenessの平均を計算
    assertiveness_transitions_average_df = df_all.groupby("cid", as_index=False)["assertiveness"].mean()

    assertiveness_transitions_average_df = assertiveness_transitions_average_df.rename(columns={"assertiveness": "AverageAssertiveness"})

    return assertiveness_transitions_average_df

def main(args):

    #ファイルのパス
    base_directory = "data/実験_アサーティブの遷移/03実験後データ/" #コードからの相対パス

    # print(load_csv(base_directory))

    # print(calc(load_csv(base_directory)))

    sorted_df = calc(load_csv(base_directory))

    #出力
    sorted_df.to_csv("average_assertiveness.csv", index=False)
    print("✅ 出力完了: average_assertiveness.csv")

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))