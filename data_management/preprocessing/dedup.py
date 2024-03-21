import argparse
import json
from hojichar import document_filters, deduplication, Compose, Document
import os
from datetime import datetime


# 説明: このスクリプトは、入力ディレクトリにあるJSONLファイルを読み込み、それぞれのファイルに対して重複除去を行います。
def exec_hojichar_deduplication(lines: list[str], output_base: str, stats: list[dict]): 
    remained_lines = [] # 重複除去後の行を格納するリスト
    cleaner = Compose([
        document_filters.JSONLoader(ignore=True), # JSONLファイルを読み込む
        deduplication.GenerateDedupLSH(), # LSHを用いて重複除去を行う
        deduplication.LSHDeduplicator( # LSHを用いて重複除去を行う
            online_dedup=True, # オンライン重複除去を行う
            store_blacklist=True # ブラックリストを保存する
        ),
        document_filters.JSONDumper() # JSONLファイルに書き込む
    ])

    # 重複除去を行い、結果をファイルに書き込む
    with open(os.path.join(output_base, "result.dedup.jsonl"), "w") as writer:
        with open(os.path.join(output_base, "rejected.dedup.jsonl"), "w") as rejected:
            for line in lines:
                result = cleaner.apply(Document(line)) # 重複除去を行う
                if result.is_rejected: # 重複と判定された場合
                    rejected.write(result.text + "\n") # rejected.dedup.jsonlに書き込む
                else: # 重複と判定されなかった場合
                    writer.write(result.text + "\n") # result.dedup.jsonlに書き込む
                    remained_lines.append(result.text) # remained_linesに追加する

    # 統計情報をファイルに書き込む
    with open(os.path.join(output_base, "stat.dedup.jsonl"), "w") as writer: 
        writer.write(json.dumps(cleaner.statistics, ensure_ascii=False) + "\n") # 統計情報を書き込む
    stats.append(cleaner.statistics) # 統計情報をstatsに追加する

    return remained_lines

# 説明: この関数は、入力ディレクトリにあるJSONLファイルを読み込み、それぞれのファイルに対して重複除去を行います。
def dedup_minhashlsh(input_dir: str, output_base: str):
    os.makedirs(output_base, exist_ok=True)
    remained_lines, stats = [], []
    for input_file in os.listdir(input_dir): # 途中から始めるならこの辺りに処理を加える（存在するファイルをスキップする）
        if not input_file.endswith(".jsonl"):
            continue
        if input_file in ['82.jsonl', '50.jsonl', '49.jsonl', '98.jsonl', '7.jsonl', '9.jsonl', '52.jsonl', '83.jsonl', '21.jsonl', '90.jsonl', '68.jsonl', '1.jsonl', '43.jsonl', '24.jsonl', '44.jsonl', '0.jsonl', '81.jsonl', '80.jsonl', '15.jsonl', '57.jsonl', '31.jsonl', '41.jsonl', '96.jsonl', '55.jsonl', '13.jsonl', '95.jsonl', '6.jsonl', '42.jsonl', '53.jsonl', '69.jsonl', '5.jsonl', '29.jsonl', '46.jsonl', '63.jsonl', '35.jsonl', '11.jsonl', '28.jsonl', '99.jsonl', '65.jsonl', '51.jsonl', '32.jsonl', '36.jsonl', '64.jsonl', '33.jsonl', '61.jsonl', '45.jsonl', '8.jsonl', '34.jsonl', '10.jsonl', '66.jsonl', '30.jsonl', '38.jsonl', '48.jsonl', '73.jsonl', '77.jsonl', '60.jsonl', '89.jsonl', '47.jsonl', '22.jsonl', '86.jsonl', '93.jsonl', '16.jsonl', '59.jsonl']:
            continue

        with open(os.path.join(input_dir, input_file)) as fp:
            json_lines = fp.readlines() # JSONLファイルを読み込む

        input_file_prefix = os.path.splitext(os.path.basename(input_file))[0] # ファイル名を取得する
        output_base_for_input: str = os.path.join(output_base, input_file_prefix) # 出力ディレクトリを指定する
        os.makedirs(output_base_for_input, exist_ok=True) # 出力ディレクトリを作成する

        remained_lines.append(exec_hojichar_deduplication(
            json_lines, output_base=output_base_for_input, stats=stats)) # 重複除去を行う

    with open(os.path.join(output_base, "results.dedup.jsonl"), "w", encoding="utf8") as writer:
        for lines in remained_lines: 
            for line in lines:
                writer.write(line + "\n")  # 重複除去後の行を書き込む

    with open(os.path.join(output_base, "stats.dedup.jsonl"), "w", encoding="utf8") as writer:
        for stat in stats:
            writer.write(json.dumps(stat, ensure_ascii=False))
            writer.write("\n") # 統計情報を書き込む

# 説明: この関数は、コマンドライン引数を解析し、重複除去を行います。
def main():
    parser = argparse.ArgumentParser(description='Process some documents.') # コマンドライン引数を解析する
    parser.add_argument('--input_dir', type=str,
                        help='The input directory containing documents to process', required=True) # 入力ディレクトリを指定する
    parser.add_argument('--output_dir', type=str,
                        help='The input file containing documents to process', required=False, default="./tmp/output") # 出力ディレクトリを指定する
    args = parser.parse_args() # 設定

    start = datetime.now() # 現在の日時を取得する
    output_base = os.path.join(args.output_dir, start.strftime("%Y%m%d%H%M%S")) # 日付をもとに出力ディレクトリを指定する

    dedup_minhashlsh(input_dir=args.input_dir, output_base=output_base) # 重複除去を行う


if __name__ == "__main__":
    main()
