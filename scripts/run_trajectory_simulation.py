from pathlib import Path
import json
from datetime import datetime, timedelta
import argparse
import numpy as np

from models.balloon_model import BalloonModel
from models.gas import LiftingGasType
from control.vent_schedule import VentSchedule
from initial_condition import InitialCondition
from simulation_config import SimulationConfig

from dynamics import propagator
from visualize import plot_balloon_state_history, plot_balloon_trajectry

OUTPUT_DIR = Path("docs")


def output(balloon_state_history):

    # 出力ファイルのパスを定義
    # 高度
    vertical_history_html_path = OUTPUT_DIR / "html/balloon_vertical_trajectory.html"
    vertical_history_png_path = (
        OUTPUT_DIR / "images/generated/balloon_vertical_trajectory.png"
    )

    # 水平
    horizon_trajectory_html_path = (
        OUTPUT_DIR / "html/balloon_xy_position_trajectory.html"
    )
    horizon_trajectory_png_path = (
        OUTPUT_DIR / "images/generated/balloon_xy_position_trajectory.png"
    )
    horizon_velocity_html_path = OUTPUT_DIR / "html/balloon_xy_velocity_trajectory.html"
    horizon_velocity_png_path = (
        OUTPUT_DIR / "images/generated/balloon_xy_velocity_trajectory.png"
    )
    horizon_history_html_path = (
        OUTPUT_DIR / "html/balloon_horizontal_posvel_history.html"
    )
    horizon_history_png_path = (
        OUTPUT_DIR / "images/generated/balloon_horizontal_posvel_history.png"
    )

    # 体積表面積
    volume_area_html_path = OUTPUT_DIR / "html/balloon_volume_area_history.html"
    volume_area_png_path = (
        OUTPUT_DIR / "images/generated/balloon_volume_area_history.png"
    )

    # ガス(密度/質量)
    gas_state_html_path = OUTPUT_DIR / "html/balloon_gas_state_history.html"
    gas_state_png_path = OUTPUT_DIR / "images/generated/balloon_gas_state_history.png"

    # 温度
    temperature_html_path = OUTPUT_DIR / "html/balloon_temperature_history.html"
    temperature_png_path = (
        OUTPUT_DIR / "images/generated/balloon_temperature_history.png"
    )

    # epochからの経過秒数に変換
    epoch_time = balloon_state_history.time_list[0]
    time_seconds = np.array(
        [
            (time - epoch_time).total_seconds()
            for time in balloon_state_history.time_list
        ],
        dtype=float,
    )

    # 位置・速度配列
    position_array = np.array(
        balloon_state_history.position_vector_list,
        dtype=float,
    )
    velocity_array = np.array(
        balloon_state_history.velocity_vector_list,
        dtype=float,
    )

    # Z方向
    altitude = position_array[:, 2]
    vertical_velocity = velocity_array[:, 2]

    # X-Y位置
    position_x = position_array[:, 0]
    position_y = position_array[:, 1]

    # Vx-Vy速度
    velocity_x = velocity_array[:, 0]
    velocity_y = velocity_array[:, 1]

    # HTMLとPNGを保存
    # 高度
    plot_balloon_trajectry.save_position_trajectory_html(
        time_seconds,
        altitude,
        vertical_velocity,
        vertical_history_html_path,
    )
    plot_balloon_trajectry.save_trajectory_png(
        time_seconds,
        altitude,
        vertical_velocity,
        vertical_history_png_path,
    )

    # 水平
    plot_balloon_trajectry.save_xy_position_trajectory_html(
        position_x,
        position_y,
        horizon_trajectory_html_path,
    )
    plot_balloon_trajectry.save_xy_position_trajectory_png(
        position_x,
        position_y,
        horizon_trajectory_png_path,
    )

    plot_balloon_trajectry.save_xy_velocity_trajectory_html(
        velocity_x,
        velocity_y,
        horizon_velocity_html_path,
    )
    plot_balloon_trajectry.save_xy_velocity_trajectory_png(
        velocity_x,
        velocity_y,
        horizon_velocity_png_path,
    )
    plot_balloon_trajectry.save_horizontal_position_velocity_html(
        time_seconds,
        position_x,
        position_y,
        velocity_x,
        velocity_y,
        horizon_history_html_path,
    )
    plot_balloon_trajectry.save_horizontal_position_velocity_png(
        time_seconds,
        position_x,
        position_y,
        velocity_x,
        velocity_y,
        horizon_history_png_path,
    )
    # 体積断面積
    plot_balloon_state_history.save_volume_area_history_html(
        time_seconds,
        balloon_state_history.volume_list,
        balloon_state_history.cross_sectional_area_list,
        volume_area_html_path,
    )
    plot_balloon_state_history.save_volume_area_history_png(
        time_seconds,
        balloon_state_history.volume_list,
        balloon_state_history.cross_sectional_area_list,
        volume_area_png_path,
    )
    # ガス
    plot_balloon_state_history.save_gas_state_history_html(
        time_seconds,
        balloon_state_history.gas_density_list,
        balloon_state_history.gas_mass_list,
        gas_state_html_path,
    )
    plot_balloon_state_history.save_gas_state_history_png(
        time_seconds,
        balloon_state_history.gas_density_list,
        balloon_state_history.gas_mass_list,
        gas_state_png_path,
    )

    # 温度
    plot_balloon_state_history.save_temperature_history_html(
        time_seconds,
        balloon_state_history.gas_temperature_list,
        temperature_html_path,
    )
    plot_balloon_state_history.save_temperature_history_png(
        time_seconds,
        balloon_state_history.gas_temperature_list,
        temperature_png_path,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run balloon trajectory simulation.")

    parser.add_argument(
        "config_path",
        nargs="?",
        default="config.json",
        help="Path to configuration JSON file. Default: config.json",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config_path)

    # balloon model
    balloon_cfg = config["balloon"].copy()
    balloon_cfg["gas_type"] = LiftingGasType[balloon_cfg["gas_type"]]

    # BalloonModel には入れない値を抜く
    initial_volume = float(balloon_cfg.pop("ground_volume"))
    initial_gas_mass = float(balloon_cfg.pop("initial_gas_mass"))
    initial_gas_temperature = float(balloon_cfg.pop("initial_gas_temperature"))
    raw_vent_schedule = balloon_cfg.pop("vent_schedule", [])

    balloon = BalloonModel(**balloon_cfg)

    # vent schedule
    vent_schedule = parse_vent_schedule_datetime(raw_vent_schedule)

    # wind condition
    # まずは無風条件 [m/s]
    wind_vector = np.array([2.0, 2.0, 0.0], dtype=float)

    # initial conditions
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

    # simulation config
    calc_cfg = config["calculate"]

    simulation_config = SimulationConfig(
        time_step=timedelta(seconds=calc_cfg["time_step_seconds"]),
        save_state_interval=timedelta(seconds=calc_cfg["save_state_interval_seconds"]),
        propagation_time=timedelta(seconds=calc_cfg["propagation_duration_seconds"]),
    )

    # simulation
    balloon_state_history = propagator.propagate(
        simulation_config,
        initial_conditions,
        balloon,
        vent_schedule,
        wind_vector,
    )

    # output
    output(balloon_state_history)


if __name__ == "__main__":
    main()
