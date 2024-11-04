from app.config import OUTPUTS_DIR
from openai import OpenAI
from pydub import AudioSegment

import random
from configparser import ConfigParser


class Text2Speech:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key)
        self.voices = {"トム": "alloy", "ジェーン": "nova"}

    def _generate_speech(self, description: str, voice: str):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
            input=description,
        )
        return response

    def _parse_scripts(self, filepath: str):
        scripts = []
        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n", "").replace("「", "").replace("」", "")
                if line != "":
                    try:
                        line_ = line.split("：")
                        character = line_[0]
                        text = line_[1]
                    except:
                        continue

                    script = {"character": character, "text": text}
                    scripts.append(script)
        return scripts

    def text_to_speech(
        self,
        script_filepath: str,
        output_filepath: str = f"{OUTPUTS_DIR}/final_output.mp3",
    ):
        script = self._parse_scripts(script_filepath)
        audio_files = []
        for i, line in enumerate(script):
            print(f"\t------ {i+1} / {len(script)} ------")
            character = line["character"]
            text = line["text"]
            voice = self.voices[character]

            print(f"\t\tGenerating speech for {character}: {text}")
            # APIで音声を生成
            audio_response = self._generate_speech(text, voice)

            # 音声ファイルを保存
            audio_filename = f"{OUTPUTS_DIR}/tmp/line_{i}.mp3"
            audio_response.stream_to_file(audio_filename)
            audio_files.append(audio_filename)
            print(f"\t\tSaved audio for {character} as {audio_filename}")

        # 発話を結合し一つの音声ファイルにエクスポート
        print("\t\taudio file combining...")
        combined_audio = AudioSegment.empty()
        for audio_file in audio_files:
            audio_segment = AudioSegment.from_mp3(audio_file)
            combined_audio += audio_segment

            # 対話における間の調整のため無音の長さを0.3〜0.7秒の範囲でランダムに差し込み
            silence_duration = random.uniform(0.3, 0.7) * 1000
            silence = AudioSegment.silent(duration=silence_duration)
            combined_audio += silence

        # 結合した音声を保存
        combined_audio.export(output_filepath, format="mp3")
        print(f"[4/5] 読み上げ音声作成完了: {output_filepath}")


if __name__ == "__main__":
    config = ConfigParser()
    config.read("../../config.ini")
    api_key = config["openai"]["API_KEY"]
    a = Text2Speech(api_key=api_key)
    a.text_to_speech(
        script_filepath="../../textfile.txt",
        output_filepath=f"{OUTPUTS_DIR}/tmp_final.mp3",
    )
