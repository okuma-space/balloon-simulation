import systems.balloon as balloon
import environment.atmosphere.isothermal_model as isothermal_model
import numpy as np
import physics.fluid_mechanics as fluid_mechanics
import phys_const
from dynamics.trajectory import Trajectory
from datetime import datetime, timedelta


def propagate(
    balloon: balloon.Balloon,
    epoch_time: datetime,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    time_step: timedelta,
    propagation_time: timedelta,
) -> Trajectory:
    """
    指定された propagation_time にわたって気球の鉛直ダイナミクスをシミュレートします。

    Parameters
    ----------
    balloon : balloon.Balloon
        気球のプロパティを含む気球オブジェクト。
    epoch_time : datetime
        propagator の開始時刻。
    initial_position : np.ndarray
        初期位置ベクトル [x, y, z] [m]。
    initial_velocity : np.ndarray
        初期速度ベクトル [vx, vy, vz] [m/s]。
    time_step : timedelta
        propagator 反復のタイムステップ。
    propagation_time : timedelta
        propagator の総時間。

    Returns
    -------
    Trajectory
        気球の時刻、位置、速度の履歴を含む Trajectory オブジェクト。
    """

    # propagatorの初期化
    time_list = [epoch_time]
    position_vector_list = [initial_position.copy()]
    velocity_vector_list = [initial_velocity.copy()]
    current_time = epoch_time
    end_time = epoch_time + propagation_time
    time_step_seconds = time_step.total_seconds()  # タイムステップを秒に変換
    cross_sectional_area = balloon.cross_section_area  # 気球の断面積[m^2]を取得

    # propagationループ
    while current_time < end_time:
        # 加速度[m/s^2]の計算
        acceleration = calculate_vertical_acceleration(
            balloon,
            position_vector_list[-1],
            velocity_vector_list[-1],
            cross_sectional_area,
        )

        # 簡単なオイラー法で位置と速度を更新する
        velocity = velocity_vector_list[-1] + acceleration * time_step_seconds
        position = position_vector_list[-1] + velocity * time_step_seconds

        # 時刻を保存
        current_time += time_step

        # 更新された時刻と位置と速度を保存
        time_list.append(current_time)
        position_vector_list.append(position)
        velocity_vector_list.append(velocity)

    return Trajectory(time_list, position_vector_list, velocity_vector_list)


def calculate_vertical_acceleration(
    balloon: balloon.Balloon,
    position_vector: np.ndarray,
    velocity_vector: np.ndarray,
    cross_sectional_area: float,
) -> np.ndarray:
    """
    気球の浮力と重力に基づいて気球の鉛直加速度を計算する。

    Parameters
    ----------
    balloon : balloon.Balloon
        気球オブジェクト。
    position_vector : np.ndarray
        位置ベクトル [x, y, z] [m]
    velocity_vector : np.ndarray
        速度ベクトル [vx, vy, vz] [m/s]
    cross_sectional_area : float
        気球の断面積 [m^2]

    Returns
    -------
    np.ndarray
        加速度ベクトル [ax, ay, az] [m/s^2]
    """

    # 大気密度[kg/m^3]を計算
    altitude = position_vector[2]  # 高度[m]
    air_density = isothermal_model.calculate_density(altitude)

    # 浮力[N]を計算
    buoyant_force = fluid_mechanics.buoyant_force(
        air_density, balloon.gas_density, balloon.volume
    )

    # 抗力[N]を計算
    # 風力は一旦0.0[m/s]固定で計算する
    drag_force = fluid_mechanics.drag_force(
        air_density,
        [0.0, 0.0, 0.0],
        velocity_vector,
        balloon.drag_coefficient,
        cross_sectional_area,
    )[2]  # 鉛直方向の抗力のみを考慮

    # 合力(ネットフォース)[N]を計算する
    # 浮力[N] + 抗力[N] -重力[N] = ネットフォース[N]
    net_force = (
        buoyant_force + drag_force - balloon.mass * phys_const.GRAVITY_ACCELERATION
    )
    # print(f"Altitude: {altitude:.2f} m, Air Density: {air_density:.4f} kg/m^3, Buoyant Force: {buoyant_force:.2f} N, Drag Force: {drag_force:.2f} N, Net Force: {net_force:.2f} N")

    # 加速度[m/s^2]を計算
    # ネットフォース[N] / 質量[kg] = 加速度[m/s^2]
    if balloon.mass == 0:
        raise ValueError("Balloon mass must not be zero to avoid division by zero.")
    acceleration = net_force / balloon.mass
    acceleration_vector = np.array([0.0, 0.0, acceleration])

    return acceleration_vector
