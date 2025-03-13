from typing import Callable, Literal

import numpy as np
import re

from fastrtc.reply_on_pause import (
    AlgoOptions,
    AppState,
    ModelOptions,
    PauseDetectionModel,
    ReplyFnGenerator,
    ReplyOnPause,
)
from fastrtc.speech_to_text import get_stt_model, stt_for_chunks
from fastrtc.utils import audio_to_float32


class WalkieTalkie(ReplyOnPause):
    def __init__(
        self,
        fn: ReplyFnGenerator,
        startup_fn: Callable | None = None,
        algo_options: AlgoOptions | None = None,
        model_options: ModelOptions | None = None,
        can_interrupt: bool = True,
        expected_layout: Literal["mono", "stereo"] = "mono",
        output_sample_rate: int = 24000,
        output_frame_size: int = 480,
        input_sample_rate: int = 48000,
        model: PauseDetectionModel | None = None,
    ):
        super().__init__(
            fn,
            algo_options=algo_options,
            startup_fn=startup_fn,
            model_options=model_options,
            can_interrupt=can_interrupt,
            expected_layout=expected_layout,
            output_sample_rate=output_sample_rate,
            output_frame_size=output_frame_size,
            input_sample_rate=input_sample_rate,
            model=model,
        )
        self.algo_options.audio_chunk_duration = 3.0
        self.state = AppState()
        self.stt_model = get_stt_model("moonshine/base")

    def over_detected(self, text: str) -> bool:
        return bool(re.search(r"\bover[.,!?]*$", text.lower()))

    def determine_pause(  # type: ignore
        self, audio: np.ndarray, sampling_rate: int, state: AppState
    ) -> bool:
        """Take in the stream, determine if a pause happened"""
        import librosa

        duration = len(audio) / sampling_rate

        if duration >= self.algo_options.audio_chunk_duration:
            audio_f32 = audio_to_float32((sampling_rate, audio))
            audio_rs = librosa.resample(
                audio_f32, orig_sr=sampling_rate, target_sr=16000
            )
            _, chunks = self.model.vad(
                (16000, audio_rs),
                self.model_options,
            )
            text = stt_for_chunks(self.stt_model, (16000, audio_rs), chunks)
            state.buffer = None
            if self.over_detected(text):
                state.stream = audio
                return True
            state.stream = None
        return False

    def reset(self):
        super().reset()
        self.generator = None
        self.event.clear()
        self.state = AppState()

    def copy(self):
        return WalkieTalkie(
            self.fn,
            self.startup_fn,
            self.algo_options,
            self.model_options,
            self.can_interrupt,
            self.expected_layout,
            self.output_sample_rate,
            self.output_frame_size,
            self.input_sample_rate,
            self.model,
        )


__all__ = ["WalkieTalkie"]
