from .constants import FrameType


class StartAttr:
    frame_attr: FrameType

    def __init__(self, frame_attr: FrameType) -> None:
        self.frame_attr = frame_attr

    def __json__(self):
        return {
            "frame_attr": self.frame_attr.value,
        }

    def __text__(self) -> str:
        return ""
