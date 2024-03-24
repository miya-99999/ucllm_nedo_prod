#!/bin/bash

# Google Driveの対象フォルダのパスを指定
base_path="output/20240320041037"

# 'filtered' ディレクトリの確認と作成
mkdir -p "${base_path}/filtered"

# 対象フォルダ内のすべてのサブフォルダをループ
find "${base_path}" -mindepth 1 -maxdepth 1 -type d | while read folder; do
    file_path="${folder}/result.dedup.jsonl"
    # 'result.filtering.jsonl' ファイルが存在するか確認
    if [ -f "${file_path}" ]; then
        # ファイル名をサブフォルダ名に基づいて設定
        filename=$(basename "${folder}").jsonl
        # ファイルを 'filtered' ディレクトリに移動
        mv "${file_path}" "${base_path}/filtered/${filename}"
    fi
done

