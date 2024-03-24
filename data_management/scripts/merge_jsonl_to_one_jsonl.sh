#!/bin/bash

# Google Driveの対象フォルダのパスを指定
base_path="output/20240320041037"

# 出力ファイルパス
output_file="output/ja/wikipedia/preprocessed_wikipedia.jsonl"

# 出力ファイルが既に存在する場合は削除
rm -f "${output_file}"

# 'find' コマンドでフォルダ内の全ての .jsonl ファイルを検索し、
# 'cat' コマンドでその内容を出力ファイルに追加
find "${base_path}" -mindepth 2 -maxdepth 2 -type f -name '*.jsonl' | while read file; do
    cat "${file}" >> "${output_file}"
done
