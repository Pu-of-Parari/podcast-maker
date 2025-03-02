import requests
from bs4 import BeautifulSoup


def get_contents_from_url(url: str = "", output_file: str = "output.txt"):
    # ページの内容を取得
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"ページの取得に失敗しました。ステータスコード: {response.status_code}"
        )
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    title = soup.find("h1", class_="entry-title")
    if not title:
        title = soup.find("h1", class_="radar-post-page-head")
    if not title:
        title = soup.find("h1")
    if title:
        title_text = title.get_text(strip=True)
        # タイトル要素を削除して重複を防ぐ
        title.decompose()
    else:
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else ""

    markdown_content = f"# {title_text}\n\n"
    content_classes = [
        "div.post-radar-content p",
        "article-content",
        "post-content",
        "entry-content",
        "content",
        "main-content",
        "post-body",
        "post",
        "article-body",
        "post-entry",
    ]
    article = None
    for class_name in content_classes:
        article = soup.select(class_name)  # 該当するクラスの複数の要素を取得
        if article:
            break
    if not article:
        article = soup.find("article")
    if not article:
        article = soup.find("div", {"id": "main-content"})
    if not article:
        # <p>、<h2>などのタグをすべて抽出
        article = soup.find_all(
            ["h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "pre", "code", "blockquote"]
        )

    added_texts = set()
    if isinstance(article, list):
        markdown_content = "\n".join([p.get_text(strip=True) for p in article])
    elif article:
        markdown_content += parse_element_to_markdown(article, added_texts)
    else:
        markdown_content += ""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        print(f"[1/5] 記事取得完了: {title_text}")

    return title_text, markdown_content


def parse_element_to_markdown(element, added_texts=None):
    if added_texts is None:
        added_texts = set()
    markdown = ""
    for child in element.contents:
        if isinstance(child, str):
            text = child.strip()
            if text and text not in added_texts:
                markdown += text
                added_texts.add(text)
        elif child.name:
            # テキストを取得し、重複をチェック
            text = child.get_text(strip=True)
            if text and text not in added_texts:
                if child.name == "h1":
                    # タイトルと重複する可能性があるためスキップ
                    continue
                elif child.name == "h2":
                    markdown += f"\n\n## {text}\n\n"
                elif child.name == "h3":
                    markdown += f"\n\n### {text}\n\n"
                elif child.name == "h4":
                    markdown += f"\n\n#### {text}\n\n"
                elif child.name == "h5":
                    markdown += f"\n\n##### {text}\n\n"
                elif child.name == "h6":
                    markdown += f"\n\n###### {text}\n\n"
                elif child.name == "p":
                    markdown += f"{text}\n\n"
                elif child.name == "ul":
                    markdown += f"\n"
                    for li in child.find_all("li", recursive=False):
                        li_text = li.get_text(strip=True)
                        if li_text and li_text not in added_texts:
                            markdown += f"- {li_text}\n"
                            added_texts.add(li_text)
                    markdown += "\n"
                # elif child.name == "ol":
                #    # 数字付きリストは内容よりも目次部分を取得することのほうが多いためskip
                #    for idx, li in enumerate(child.find_all("li", recursive=False), 1):
                #        li_text = li.get_text(strip=True)
                #        if li_text and li_text not in added_texts:
                #            markdown += f"{idx}. {li_text}\n"
                #            added_texts.add(li_text)
                #    markdown += "\n"
                elif child.name == "pre":
                    code = child.get_text()
                    if code and code not in added_texts:
                        markdown += f"\n\n```\n{code}\n```\n\n"
                        added_texts.add(code)
                elif child.name == "code":
                    code = child.get_text(strip=True)
                    if code and code not in added_texts:
                        markdown += f"`{code}`"
                        added_texts.add(code)
                elif child.name == "blockquote":
                    quote = child.get_text(strip=True)
                    if quote and quote not in added_texts:
                        markdown += f"\n\n> {quote}\n\n"
                        added_texts.add(quote)
                else:
                    # 他のタグは再帰的に処理
                    markdown += parse_element_to_markdown(child, added_texts)
                added_texts.add(text)
            else:
                # 子要素を再帰的に処理
                markdown += parse_element_to_markdown(child, added_texts)
    return markdown


if __name__ == "__main__":
    url = ""
    title, markdown_content = get_contents_from_url(url)
