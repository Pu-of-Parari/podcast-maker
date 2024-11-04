from pydub import AudioSegment
from app.config import OUTPUTS_DIR, BGM_FILE


class AddBgm:
    def __init__(self) -> None:
        self.TIME_SCRIPT_IN = 8500  # 会話が始まるタイミング(ms)
        self.TIME_BGM_OUT = 5000  # BGMが終了する際のフェードアウト時間(ms)

    def add_bgm(
        self,
        script_filepath: str = f"{OUTPUTS_DIR}/tmp_final.mp3",
        bgm_filepath: str = "",
        output_filepath: str = f"{OUTPUTS_DIR}/tmp_final_with_bgm.mp3",
    ):
        script = AudioSegment.from_mp3(script_filepath)

        if not bgm_filepath:
            bgm_filepath = BGM_FILE
        bgm = AudioSegment.from_mp3(bgm_filepath)

        # 音量とスピード調整
        bgm = bgm.apply_gain(-10)
        script = script.apply_gain(5)
        # memo: openaiのモデルは若干話すスピードが遅かったため1.1倍で調整
        script = script.speedup(playback_speed=1.1)

        # スクリプトが始まるタイミングでBGMの音量を10db下げる
        bgm_intro = bgm[: self.TIME_SCRIPT_IN]
        bgm_rest = bgm[self.TIME_SCRIPT_IN :].apply_gain(-10)

        # BGMをscriptの長さに合わせてループ再生
        bgm_loop_duration = len(script) + self.TIME_BGM_OUT  # bgmの全体再生時間
        bgm_loop = bgm_rest * (bgm_loop_duration // len(bgm_rest) + 1)
        bgm_loop = bgm_loop[:bgm_loop_duration]

        # script再生終了後のフェードアウト
        bgm_with_fadeout = bgm_loop.fade_out(self.TIME_BGM_OUT)
        combined_bgm = bgm_intro + bgm_with_fadeout

        # scriptとBGMをミックス
        # memo: 自然な入りになるようにbgmの音量が下がった1000ms後にスクリプト再生するよう調整
        combined_audio = combined_bgm.overlay(
            script, position=self.TIME_SCRIPT_IN + 1000
        )

        # 最終的な音声ファイルを保存
        combined_audio.export(output_filepath, format="mp3")
        print(f"[5/5] podcast作成完了: {output_filepath}")


if __name__ == "__main__":
    a = AddBgm()
    a.add_bgm(
        script_filepath=f"{OUTPUTS_DIR}/tmp_final.mp3",
        output_filepath=f"{OUTPUTS_DIR}/tmp_final_with_bgm.mp3",
    )
