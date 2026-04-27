# from systems.balloon_system import BalloonSystem
# from dynamics import vertical_dynamics
# from datetime import datetime, timedelta
# from systems import gas

# # 許容誤差20[%]
# REL_TOL = 0.20


# def test_vertical_dynamics():
#     """
#     気球工学 P.16の事例に従い,記載されている科学気球モデルでの最高到達高度を検証する.
#     """
#     # 最高到達高度が35000[m]近辺であることを検証するための科学気球モデル
#     balloon = BalloonSystem(
#         payload_mass=500.0,
#         payload_area=1.0,
#         payload_drag_coefficient=1.1,
#         ground_volume=1387.0,
#         max_volume=100000.0,
#         initial_gas_mass=230.0,
#         initial_gas_temperature=288.0,
#         balloon_drag_coefficient=0.47,
#         vent_area=0.071,
#         flow_coefficient=0.61,
#         gas_type=gas.LiftingGasType.HELIUM,
#         vent_schedule=[],
#     )

#     # シミュレーションの実行
#     balloon_state_history = vertical_dynamics.propagate(
#         balloon,
#         datetime.fromisoformat("2026-01-01T00:00:00Z".replace("Z", "+00:00")),
#         [0.0, 0.0, 0.0],
#         [0.0, 0.0, 0.0],
#         timedelta(seconds=1),
#         timedelta(seconds=1),
#         timedelta(seconds=3000),
#     )

#     # 高度成分のみを抜き取る
#     balloon_state_history.position_vector_list[:, 2]

#     # 最大高度が35000[m]近辺であることを検証する
#     max_altitude = balloon_state_history.position_vector_list[:, 2].max()
#     assert abs(max_altitude - 35000.0) / 35000.0 <= REL_TOL, (
#         f"Maximum altitude {max_altitude} is not within {REL_TOL * 100}% of 35000[m]"
#     )
from datetime import datetime, timedelta

from models.balloon_model import BalloonModel
from models import gas
from dynamics import vertical_dynamics
from initial_condition import InitialCondition
from simulation_config import SimulationConfig

# 許容誤差20[%]
REL_TOL = 0.20


def test_vertical_dynamics():
    """
    気球工学 P.16の事例に従い,記載されている科学気球モデルでの最高到達高度を検証する.
    """
    # 最高到達高度が35000[m]近辺であることを検証するための科学気球モデル
    balloon = BalloonModel(
        payload_mass=500.0,
        payload_area=1.0,
        payload_drag_coefficient=1.1,
        max_volume=100000.0,
        balloon_drag_coefficient=0.47,
        vent_area=0.071,
        flow_coefficient=0.61,
        gas_type=gas.LiftingGasType.HELIUM,
    )

    # 初期条件
    initial_condition = InitialCondition(
        epoch_time=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        position=[0.0, 0.0, 0.0],
        velocity=[0.0, 0.0, 0.0],
        volume=1387.0,
        gas_mass=230.0,
        gas_temperature=288.0,
    )

    # シミュレーション条件
    simulation_config = SimulationConfig(
        time_step=timedelta(seconds=1),
        save_state_interval=timedelta(seconds=1),
        propagation_time=timedelta(seconds=3000),
    )

    from control.vent_schedule import VentSchedule

    vent_schedule = VentSchedule(windows=[])

    # シミュレーションの実行
    balloon_state_history = vertical_dynamics.propagate(
        simulation_config, initial_condition, balloon, vent_schedule
    )

    # 最大高度が35000[m]近辺であることを検証する
    max_altitude = balloon_state_history.position_vector_list[:, 2].max()
    assert abs(max_altitude - 35000.0) / 35000.0 <= REL_TOL, (
        f"Maximum altitude {max_altitude} is not within {REL_TOL * 100}% of 35000[m]"
    )
