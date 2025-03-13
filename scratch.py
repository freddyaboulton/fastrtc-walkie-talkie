from fastrtc_walkie_talkie import WalkieTalkie
from fastrtc import Stream
from numpy.typing import NDArray
import numpy as np

def echo(audio: tuple[int, NDArray[np.int16]]):
    """Echo the audio back to the user after they say a sentence ending with "over"."""
    yield audio


stream = Stream(
    handler=WalkieTalkie(echo),
    modality="audio",
    mode="send-receive",
    ui_args={"title": "Walkie Talkie Turn Taking Algorithm",
            "subtitle": "Say 'over' to finish your turn. For example, 'Hi, how are you? over'."},
)

stream.ui.launch()