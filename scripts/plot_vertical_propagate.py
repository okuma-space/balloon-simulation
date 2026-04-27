# from pathlib import Path
# import numpy as np
# from datetime import datetime, timedelta
# from systems.balloon_system import BalloonSystem
# import dynamics.vertical_dynamics as vertical_dynamics
# import json
# from systems.gas import LiftingGasType
# from visualize import plot_balloon_state_history, plot_balloon_trajectry

# OUTPUT_DIR = Path("docs")


# def simulate_balloon_trajectory(
#     balloon: BalloonSystem,
#     epoch_time: datetime,
#     initial_position: np.ndarray,
#     initial_velocity: np.ndarray,
#     time_step: timedelta,
#     save_state_interval: timedelta,
#     propagation_time: timedelta,
# ) -> tuple[np.ndarray, np.ndarray]:
#     """指定されたpropagation_timeにわたって気球の鉛直ダイナミクスをシミュレートし、stateの配列を返す。"""
#     traj = vertical_dynamics.propagate(
#         balloon,
#         epoch_time,
#         initial_position,
#         initial_velocity,
#         time_step,
#         save_state_interval,
#         propagation_time,
#     )
#     # 時刻,位置,速度の配列を取得
#     # 時刻はepoch_timeからの経過秒数に変換
#     times = np.array([(t - epoch_time).total_seconds() for t in traj.time_list])
#     positions = np.array(traj.position_vector_list)
#     velocities = np.array(traj.velocity_vector_list)

#     # 高度と鉛直速度を抽出
#     altitude = positions[:, 2]
#     vertical_velocity = velocities[:, 2]

#     return (
#         times,
#         altitude,
#         vertical_velocity,
#         traj.volume_list,
#         traj.gas_density_list,
#         traj.gas_mass_list,
#         traj.gas_temperature_list,
#         traj.cross_sectional_area_list,
#     )


# def parse_vent_schedule_datetime(
#     raw_schedule: list[list[str]],
# ) -> list[tuple[datetime, datetime]]:
#     return [
#         (
#             datetime.fromisoformat(start.replace("Z", "+00:00")),
#             datetime.fromisoformat(end.replace("Z", "+00:00")),
#         )
#         for start, end in raw_schedule
#     ]


# def load_config(path: str) -> dict:
#     with open(path, "r") as f:
#         return json.load(f)


# def main():
#     config = load_config("config.json")

#     # configからBalloonSystemオブジェクトを作成
#     balloon_cfg = config["balloon"]
#     balloon_cfg["gas_type"] = LiftingGasType[balloon_cfg["gas_type"]]
#     balloon_cfg["vent_schedule"] = parse_vent_schedule_datetime(
#         balloon_cfg["vent_schedule"]
#     )
#     balloon = BalloonSystem(**balloon_cfg)

#     # trajectoryの初期条件をconfigから読み込む
#     traj_cfg = config["trajectory"]

#     epoch = datetime.fromisoformat(traj_cfg["epoch"].replace("Z", "+00:00"))

#     initial_position = np.array(traj_cfg["initial_position"], dtype=float)
#     initial_velocity = np.array(traj_cfg["initial_velocity"], dtype=float)

#     # 計算条件をconfigから読み込む
#     calc_cfg = config["calculate"]

#     time_step = timedelta(seconds=calc_cfg["time_step_seconds"])
#     save_state_interval = timedelta(seconds=calc_cfg["save_state_interval_seconds"])
#     propagation_duration = timedelta(seconds=calc_cfg["propagation_duration_seconds"])

#     # simulation
#     (
#         time_seconds,
#         altitude,
#         vertical_velocity,
#         volume,
#         gas_density,
#         gas_mass,
#         gas_temperature,
#         area,
#     ) = simulate_balloon_trajectory(
#         balloon,
#         epoch,
#         initial_position,
#         initial_velocity,
#         time_step,
#         save_state_interval,
#         propagation_duration,
#     )

#     # 出力ファイルのパスを定義
#     html_path = OUTPUT_DIR / "html/balloon_posvel_trajectory.html"
#     png_path = OUTPUT_DIR / "png/balloon_posvel_trajectory.png"
#     volume_area_html_path = OUTPUT_DIR / "html/balloon_volume_area_history.html"
#     volume_area_png_path = OUTPUT_DIR / "png/balloon_volume_area_history.png"
#     gas_state_html_path = OUTPUT_DIR / "html/balloon_gas_state_history.html"
#     gas_state_png_path = OUTPUT_DIR / "png/balloon_gas_state_history.png"
#     temperature_html_path = OUTPUT_DIR / "html/balloon_temperature_history.html"
#     temperature_png_path = OUTPUT_DIR / "png/balloon_temperature_history.png"

#     # HTMLとPNGを保存
#     plot_balloon_trajectry.save_position_trajectory_html(
#         time_seconds, altitude, vertical_velocity, html_path
#     )
#     plot_balloon_trajectry.save_trajectory_png(
#         time_seconds, altitude, vertical_velocity, png_path
#     )

#     plot_balloon_state_history.save_volume_area_history_html(
#         time_seconds,
#         volume,
#         area,
#         volume_area_html_path,
#     )

#     plot_balloon_state_history.save_volume_area_history_png(
#         time_seconds,
#         volume,
#         area,
#         volume_area_png_path,
#     )

#     plot_balloon_state_history.save_gas_state_history_html(
#         time_seconds,
#         gas_density,
#         gas_mass,
#         gas_state_html_path,
#     )
#     plot_balloon_state_history.save_gas_state_history_png(
#         time_seconds,
#         gas_density,
#         gas_mass,
#         gas_state_png_path,
#     )

#     plot_balloon_state_history.save_temperature_history_html(
#         time_seconds,
#         gas_temperature,
#         temperature_html_path,
#     )
#     plot_balloon_state_history.save_temperature_history_png(
#         time_seconds,
#         gas_temperature,
#         temperature_png_path,
#     )


# if __name__ == "__main__":
#     main()
from pathlib import Path
import json
from datetime import datetime, timedelta

import numpy as np

from models.balloon_model import BalloonModel
from models.gas import LiftingGasType
from control.vent_schedule import VentSchedule
from initial_condition import InitialCondition
from simulation_config import SimulationConfig

import dynamics.vertical_dynamics as vertical_dynamics
from visualize import plot_balloon_state_history, plot_balloon_trajectry


OUTPUT_DIR = Path("docs")


def simulate_balloon_trajectory(
    balloon: BalloonModel,
    initial_conditions: InitialCondition,
    simulation_config: SimulationConfig,
    vent_schedule: VentSchedule,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """
    指定された propagation_time にわたって気球の鉛直ダイナミクスをシミュレートし、
    state の履歴配列を返す。
    """
    traj = vertical_dynamics.propagate(
        balloon,
        initial_conditions,
        simulation_config,
        vent_schedule,
    )

    # 時刻, 位置, 速度の配列を取得
    # 時刻は epoch_time からの経過秒数に変換
    time_seconds = np.array(
        [
            (state.time - initial_conditions.epoch_time).total_seconds()
            for state in traj.states
        ],
        dtype=float,
    )
    positions = np.array(
        [state.position_vector for state in traj.states],
        dtype=float,
    )
    velocities = np.array(
        [state.velocity_vector for state in traj.states],
        dtype=float,
    )

    # 高度と鉛直速度を抽出
    altitude = positions[:, 2]
    vertical_velocity = velocities[:, 2]

    volume = np.array([state.volume for state in traj.states], dtype=float)
    gas_density = np.array([state.gas_density for state in traj.states], dtype=float)
    gas_mass = np.array([state.gas_mass for state in traj.states], dtype=float)
    gas_temperature = np.array(
        [state.gas_temperature for state in traj.states],
        dtype=float,
    )
    area = np.array(
        [state.cross_sectional_area for state in traj.states],
        dtype=float,
    )

    return (
        time_seconds,
        altitude,
        vertical_velocity,
        volume,
        gas_density,
        gas_mass,
        gas_temperature,
        area,
    )


def parse_vent_schedule_datetime(
    raw_schedule: list[list[str]],
) -> VentSchedule:
    windows = tuple(
        (
            datetime.fromisoformat(start.replace("Z", "+00:00")),
            datetime.fromisoformat(end.replace("Z", "+00:00")),
        )
        for start, end in raw_schedule
    )
    return VentSchedule(windows=windows)


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config("config.json")

    # -----------------------------
    # balloon model
    # -----------------------------
    balloon_cfg = config["balloon"].copy()
    balloon_cfg["gas_type"] = LiftingGasType[balloon_cfg["gas_type"]]

    # BalloonModel には入れない値を抜く
    initial_volume = float(balloon_cfg.pop("ground_volume"))
    initial_gas_mass = float(balloon_cfg.pop("initial_gas_mass"))
    initial_gas_temperature = float(balloon_cfg.pop("initial_gas_temperature"))
    raw_vent_schedule = balloon_cfg.pop("vent_schedule", [])

    balloon = BalloonModel(**balloon_cfg)

    # -----------------------------
    # vent schedule
    # -----------------------------
    vent_schedule = parse_vent_schedule_datetime(raw_vent_schedule)

    # -----------------------------
    # initial conditions
    # -----------------------------
    traj_cfg = config["trajectory"]

    epoch_time = datetime.fromisoformat(traj_cfg["epoch"].replace("Z", "+00:00"))

    initial_conditions = InitialCondition(
        epoch_time=epoch_time,
        position=np.array(traj_cfg["initial_position"], dtype=float),
        velocity=np.array(traj_cfg["initial_velocity"], dtype=float),
        volume=initial_volume,
        gas_mass=initial_gas_mass,
        gas_temperature=initial_gas_temperature,
    )

    # -----------------------------
    # simulation config
    # -----------------------------
    calc_cfg = config["calculate"]

    simulation_config = SimulationConfig(
        time_step=timedelta(seconds=calc_cfg["time_step_seconds"]),
        save_state_interval=timedelta(seconds=calc_cfg["save_state_interval_seconds"]),
        propagation_time=timedelta(seconds=calc_cfg["propagation_duration_seconds"]),
    )

    # -----------------------------
    # simulation
    # -----------------------------
    (
        time_seconds,
        altitude,
        vertical_velocity,
        volume,
        gas_density,
        gas_mass,
        gas_temperature,
        area,
    ) = simulate_balloon_trajectory(
        simulation_config,
        initial_conditions,
        balloon,
        vent_schedule,
    )

    # 出力ファイルのパスを定義
    html_path = OUTPUT_DIR / "html/balloon_posvel_trajectory.html"
    png_path = OUTPUT_DIR / "images/generated/balloon_posvel_trajectory.png"
    volume_area_html_path = OUTPUT_DIR / "html/balloon_volume_area_history.html"
    volume_area_png_path = (
        OUTPUT_DIR / "images/generated/balloon_volume_area_history.png"
    )
    gas_state_html_path = OUTPUT_DIR / "html/balloon_gas_state_history.html"
    gas_state_png_path = OUTPUT_DIR / "images/generated/balloon_gas_state_history.png"
    temperature_html_path = OUTPUT_DIR / "html/balloon_temperature_history.html"
    temperature_png_path = (
        OUTPUT_DIR / "images/generated/balloon_temperature_history.png"
    )

    # HTMLとPNGを保存
    plot_balloon_trajectry.save_position_trajectory_html(
        time_seconds,
        altitude,
        vertical_velocity,
        html_path,
    )
    plot_balloon_trajectry.save_trajectory_png(
        time_seconds,
        altitude,
        vertical_velocity,
        png_path,
    )

    plot_balloon_state_history.save_volume_area_history_html(
        time_seconds,
        volume,
        area,
        volume_area_html_path,
    )
    plot_balloon_state_history.save_volume_area_history_png(
        time_seconds,
        volume,
        area,
        volume_area_png_path,
    )

    plot_balloon_state_history.save_gas_state_history_html(
        time_seconds,
        gas_density,
        gas_mass,
        gas_state_html_path,
    )
    plot_balloon_state_history.save_gas_state_history_png(
        time_seconds,
        gas_density,
        gas_mass,
        gas_state_png_path,
    )

    plot_balloon_state_history.save_temperature_history_html(
        time_seconds,
        gas_temperature,
        temperature_html_path,
    )
    plot_balloon_state_history.save_temperature_history_png(
        time_seconds,
        gas_temperature,
        temperature_png_path,
    )


if __name__ == "__main__":
    main()
