from enum import Enum


class CardType(Enum):
    Start = "Start"
    Progress = "Progress"
    Action = "Action"
    Frame = "Frame"


class AbilityType(Enum):
    Persistent = "Persistent"
    Automatic = "Automatic"
    Activated = "Activated"


class CardColor(Enum):
    Blue = "Blue"
    Black = "Black"
    Red = "Red"
    White = "White"
    Green = "Green"


class FrameType(Enum):
    Any = "Any"
    Omega = "Omega"
    Sigma = "Sigma"
    Forall = "Forall"
