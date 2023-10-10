from .constants import FrameType


class StartAttr:
    frame: FrameType

    def __init__(self, frame: FrameType) -> None:
        self.frame = frame

    def __json__(self):
        return {
            "frame": self.frame.value,
        }

    def __text__(self) -> str:
        return f"{self.frame.value}"
