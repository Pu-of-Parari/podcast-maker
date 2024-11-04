import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image

from app.utils import get_contents_from_url as gcfu
from app.utils import prep_filtering_contents as prep
from app.utils import add_bgm
from app.utils import text2speech
from app.utils import create_script
from app.utils.podcast_info import write_info
from app.config import (
    SCRIPT_FILE,
    CONTENTS_FILE,
    FILTER_CONTENTS_FILE,
    READING_FILE,
    PODCASTS_DIR,
    ICON_IMG,
)


def to_camel_case(s: str) -> str:
    words = s.split()
    camel_case = "".join(word.capitalize() for word in words)
    return camel_case


def get_episode_num() -> int:
    audio_files = [f for f in os.listdir(PODCASTS_DIR) if f.endswith(".mp3")]
    return len(audio_files)


def main_sidebar():
    with st.container():
        with st.sidebar:
            openai_api_key = st.text_input(
                "OpenAI API Key",
                key="openai_api_key",
                type="password",
                help="input your openai key",
            )
            st.write(
                "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            )


def main_contents():
    with st.container():
        with st.form("url", clear_on_submit=False):
            url = st.text_input("作成したい記事のURLを入力してください")
            submitted = st.form_submit_button("作成")

        if not url and submitted:
            st.warning("URLを入力してください")
        if url and submitted:
            api_key = os.getenv("OPENAI_API_KEY")
            contents_filepath = CONTENTS_FILE
            filtered_filepath = FILTER_CONTENTS_FILE
            script_filepath = SCRIPT_FILE

            with st.status(
                "Podcast作成中... (作成時間目安：2分程度)", expanded=True
            ) as status:
                st.write("[1/4] Getting contents from URL...")
                title, _ = gcfu.get_contents_from_url(
                    url=url, output_file=contents_filepath
                )
                prep.filtering_contents(
                    input_filepath=contents_filepath, output_filepath=filtered_filepath
                )

                st.write("[2/4] Creating script file...")
                episode_num = get_episode_num() + 1
                title = f"Ep.{episode_num:02}_{to_camel_case(title)}"
                reading_filepath = READING_FILE
                final_filepath = f"{PODCASTS_DIR}/{title}.mp3"

                c = create_script.CreateScript(api_key=api_key)
                c.create_script(script_filepath=script_filepath)

                st.write("[3/4] Creating reading file...")
                a = text2speech.Text2Speech(api_key=api_key)
                a.text_to_speech(
                    script_filepath=script_filepath,
                    output_filepath=reading_filepath,
                )

                st.write("[4/4] Adding BGM...")
                b = add_bgm.AddBgm()
                b.add_bgm(
                    script_filepath=reading_filepath,
                    output_filepath=final_filepath,
                )

                write_info(url=url, title=title)

                status.update(
                    label=f"Created! >> {title}", state="complete", expanded=False
                )


def main():
    st.title("🎤 Podcast maker")
    main_sidebar()
    main_contents()


if __name__ == "__main__":
    load_dotenv()
    im = Image.open(ICON_IMG)
    st.set_page_config(page_title="聞く技術ブログFM", page_icon=im, layout="wide")
    main()
