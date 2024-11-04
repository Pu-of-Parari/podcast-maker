import re


def filtering_contents(input_filepath: str, output_filepath: str):
    # フィルタリングのルールを定義
    rules = [
        r"^##\s*Top comments.*",  # "## Top comments" で始まる行
        r".*[\w\.-]+@[\w\.-]+\.\w+.*",  # メールアドレスを含む行
        r"^#[^\s]*$",  # "#"で始まり、スペースを含まない行(ハッシュタグ等)
        r"infoMore than (.*?) have passed since last update\.",  # 「更新履歴が一定期間以上」
    ]

    # 下記の文言を含む場合はそれ以降の内容をカット
    stop_words = [
        "Top comments(5)",  # for dev.to
        "Go to list of users who liked",  # for qiita
        "### Discussion",  # for zenn
        "バッジを贈って著者を応援しよう",  # for zenn
    ]

    compiled_rules = [re.compile(rule, re.IGNORECASE) for rule in rules]
    filtered_lines = []

    with open(input_filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    stop_parse = False
    for line in lines:
        stripped_line = line.strip()
        for stop_word in stop_words:
            if line.find(stop_word) != -1:
                stop_parse = True
                break
        if stop_parse:
            break

        remove_line = False
        for pattern in compiled_rules:
            if pattern.match(stripped_line):
                remove_line = True
                break  # マッチしたら他のルールをチェックする必要はない

        if not remove_line:
            filtered_lines.append(line.rstrip())

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(filtered_lines))

    print(f"[2/5] フィルタリング完了: {output_filepath}")


if __name__ == "__main__":
    filtering_contents("./output.txt", output_filepath="./filter_output.md")
