import os
from datetime import datetime
import streamlit as st
from PIL import Image
from app.config import PODCASTS_DIR, THUMBNAIL_IMG, ICON_IMG
from app.utils.podcast_info import get_url_by_title, read_info


def get_audio_files(directory: str):
    audio_files = [f for f in os.listdir(directory) if f.endswith(".mp3")]
    return sorted(audio_files, reverse=True)


def get_audio_create_time(filepath: str):
    stat = os.stat(filepath)
    create_time = datetime.fromtimestamp(stat.st_ctime)
    create_time = create_time.strftime("%Y/%-m/%-d %-H:%M")
    return create_time


def container_audio_view():
    podcast_info = read_info()
    with st.container():
        audio_files = get_audio_files(PODCASTS_DIR)
        if audio_files:
            for audio_file in audio_files:
                title = audio_file.replace(".mp3", "")
                with st.expander(title, expanded=True):
                    data = f"{PODCASTS_DIR}/{audio_file}"
                    url = get_url_by_title(title=title, data=podcast_info)
                    st.audio(data, format="audio/mpeg")
                    st.write(f"Podcast更新日：{get_audio_create_time(data)}")
                    st.write(f"元記事：{url}")
        else:
            st.write("No podcasts...")


def container_explain():
    with st.expander("What is this?"):
        img = Image.open(THUMBNAIL_IMG)
        st.markdown(
            """
            ### 『聞く技術ブログFM』について
            """
        )

        st.image(img, caption="", width=300)

        st.markdown(
            """
            - 初心者エンジニアのトムとスタッフエンジニアのジェーン、2人のメンタリング風対話によるエンジニアが必要な幅広い技術知識を学ぶきっかけを作るためのラジオです。
            - コンセプト
                - このアプリの作者が興味を持ったテック系/キャリア系記事の内容を「スキマ時間に聞いてインプットすること」が目的
                - 勉強の「きっかけ作り」の場を提供。詳細まで学ぶところはスコープ外
            - 想定リスナー
                - 中級エンジニアにステップアップしたい1-5年目のソフトウェアエンジニア
            
            ※AIによる自動生成であるため、誤った内容、聞き取りにくい部分がある可能性がありますのでご了承ください。
            """
        )


def main_listening_page():
    st.title("🎧 Podcasts list")
    container_explain()
    container_audio_view()


im = Image.open(ICON_IMG)
st.set_page_config(page_title="聞く技術ブログFM", page_icon=im, layout="wide")
main_listening_page()
