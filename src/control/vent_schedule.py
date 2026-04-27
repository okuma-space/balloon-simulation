from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class VentSchedule:
    windows: tuple[tuple[datetime, datetime], ...]

    # 現在排気中か確認する
    def is_open(self, current_time: datetime) -> bool:
        return any(start <= current_time <= end for start, end in self.windows)
