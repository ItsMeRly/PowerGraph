from collections import deque
from channel import Channel

class Block:
    def __init__(self, channels: deque[Channel]) -> None:
        self.channels = channels

    def __str__(self) -> str:
        return str(list(self.channels))
