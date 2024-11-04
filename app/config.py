from pathlib import Path

# config.pyのあるディレクトリ（app/）を基準にパスを構築
APP_DIR = Path(__file__).resolve().parent
WORK_DIR = APP_DIR.parent

# 主要ディレクトリ
TEMPLATE_DIR = WORK_DIR / "app/template"
OUTPUTS_DIR = WORK_DIR / "outputs"
PODCASTS_DIR = OUTPUTS_DIR / "podcasts"

# テンプレートファイル
BGM_FILE = TEMPLATE_DIR / "morning.mp3"
THUMBNAIL_IMG = TEMPLATE_DIR / "thumbnail.png"
ICON_IMG = TEMPLATE_DIR / "icon.webp"
TEMPLATE_PROMPT_FILE = TEMPLATE_DIR / "template_prompt.txt"

# 生成ファイル
CONTENTS_FILE = OUTPUTS_DIR / "scripts/contents.txt"
FILTER_CONTENTS_FILE = OUTPUTS_DIR / "scripts/filter_contents.txt"
SCRIPT_FILE = OUTPUTS_DIR / "scripts/script.txt"
READING_FILE = OUTPUTS_DIR / "scripts/reading.mp3"
INFO_FILE = PODCASTS_DIR / "info.csv"
