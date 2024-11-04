import os
from dotenv import load_dotenv
from openai import OpenAI

from app.config import FILTER_CONTENTS_FILE, TEMPLATE_PROMPT_FILE, SCRIPT_FILE


class CreateScript:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key)

    def create_script(self, script_filepath: str = SCRIPT_FILE):
        completion = self.client.chat.completions.create(
            model="gpt-4o",  # gpt-4o-mini
            max_tokens=4500,
            n=1,
            messages=[
                {
                    "role": "system",
                    "content": self._get_template_prompt(),
                },
                {"role": "user", "content": f"<記事>: {self._get_article()}"},
            ],
        )

        content = completion.choices[0].message.content
        with open(script_filepath, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"[3/5] スクリプト作成完了: {script_filepath}")

        return completion

    def _get_template_prompt(self):
        with open(TEMPLATE_PROMPT_FILE) as f:
            template_prompt = f.read()
        return template_prompt

    def _get_article(self):
        with open(FILTER_CONTENTS_FILE) as f:
            article = f.read()
        return article


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    cd = CreateScript(api_key=api_key)
    result = cd.create_script(script_filepath="./script.txt")
