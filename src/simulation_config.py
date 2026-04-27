from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class SimulationConfig:
    time_step: timedelta  # シミュレーション計算ステップ
    save_state_interval: timedelta  # データの保存感覚
    propagation_time: timedelta  # シミュレーション伝搬時間長
