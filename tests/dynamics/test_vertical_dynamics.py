from systems.balloon_system import BalloonSystem
from dynamics import vertical_dynamics
from datetime import datetime, timedelta

# 許容誤差20[%]
REL_TOL = 0.20


def test_vertical_dynamics():
    """
    気球工学 P.16の事例に従い,記載されている科学気球モデルでの最高到達高度を検証する.
    """
    # 最高到達高度が35000[m]近辺であることを検証するための科学気球モデル
    balloon = BalloonSystem(
        payload_mass=500.0,
        ground_volume=1578.0,
        max_volume=100000.0,
        gas_mass=230.0,
        drag_coefficient=0.47,
    )

    # シミュレーションの実行
    balloon_state_history = vertical_dynamics.propagate(
        balloon,
        datetime.fromisoformat("2026-01-01T00:00:00Z".replace("Z", "+00:00")),
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        timedelta(seconds=1),
        timedelta(seconds=1),
        timedelta(seconds=3000),
    )

    # 高度成分のみを抜き取る
    balloon_state_history.position_vector_list[:, 2]  

    # 最大高度が35000[m]近辺であることを検証する
    max_altitude = balloon_state_history.position_vector_list[:, 2].max()
    assert abs(max_altitude - 35000.0) / 35000.0 <= REL_TOL, f"Maximum altitude {max_altitude} is not within {REL_TOL*100}% of 35000[m]"
