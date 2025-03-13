# ReplyOnOver FastRTC

[![PyPI - Version](https://img.shields.io/pypi/v/fastrtc-walkie-talkie.svg)](https://pypi.org/project/fastrtc-walkie-talkie)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastrtc-walkie-talkie.svg)](https://pypi.org/project/fastrtc-walkie-talkie)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install fastrtc-walkie-talkie
```

## Usage

```python
from fastrtc_walkie_talkie import WalkieTalkie
from fastrtc import Stream


def echo(audio: tuple[int, np.ndarray]):
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
```
