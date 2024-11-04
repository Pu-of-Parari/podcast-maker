import csv
from pathlib import Path

from app.config import INFO_FILE


def write_info(url: str, title: str, file_path: str = INFO_FILE) -> None:
    # ファイルが存在しない場合はヘッダーを追加
    file_exists = Path(file_path).exists()

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.witerow("\n")
            writer.writerow(["url", "title"])
        writer.writerow([url, title])


def read_info(file_path: str = INFO_FILE) -> dict:
    data = {}
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = {row["title"]: row["url"] for row in reader}
    except FileNotFoundError:
        pass
    return data


def get_url_by_title(title: str, data: dict) -> str:
    # タイトルが存在しない場合は None を返す
    return data.get(title)
