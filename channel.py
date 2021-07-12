from collections import deque


class Channel:
    def __init__(self, values: deque[float]) -> None:
        self.values = values

    def __str__(self) -> str:
        return str(list(self.values))
