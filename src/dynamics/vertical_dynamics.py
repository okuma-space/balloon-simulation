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
    指定されたpropagation_timeにわたって気球の鉛直ダイナミクスをシミュレートします。

    Args:
        balloon (balloon.Balloon): 気球のプロパティを含む気球オブジェクト。
        epoch_time (datetime): propagatorの開始時刻。
        initial_position (np.ndarray): 初期位置ベクトル [x, y, z] [m]。
        initial_velocity (np.ndarray): 初期速度ベクトル [vx, vy, vz] [m/s]。
        time_step (timedelta): propagator反復のタイムステップ。
        propagation_time (timedelta): propagatorの総時間。

    Returns:
        Trajectory: 気球の時刻、位置、速度の履歴を含むTrajectoryオブジェクト。
    """

    # propagatorの初期化
    time_list = [epoch_time]
    position_vector_list = [initial_position.copy()]
    velocity_vector_list = [initial_velocity.copy()]
    current_time = epoch_time
    end_time = epoch_time + propagation_time
    time_step_seconds = time_step.total_seconds() # タイムステップを秒に変換

    # propagationループ
    while current_time < end_time:
        # 加速度[m/s^2]の計算
        acceleration = calculate_vertical_acceleration(
            balloon, position_vector_list[-1]
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
    balloon: balloon.Balloon, position_vector: np.ndarray
) -> np.ndarray:
    """
    気球の浮力と重力に基づいて気球の鉛直加速度を計算する。

    Args:
        balloon (balloon.Balloon): 気球オブジェクト。
        position_vector (np.ndarray): 位置ベクトル [x, y, z] [m]。

    Returns:
        np.ndarray: 加速度ベクトル [ax, ay, az] [m/s^2]。
    """

    # 大気密度[kg/m^3]を計算
    altitude = position_vector[2]  # 高度[m]
    air_density = isothermal_model.calculate_density(altitude)

    # 浮力[N]を計算
    buoyant_force = fluid_mechanics.buoyant_force(
        air_density, balloon.gas_density, balloon.volume
    )

    # 合力(ネットフォース)[N]を計算する
    # 浮力[N] -重力[N] = ネットフォース[N]
    net_force = buoyant_force - balloon.mass * phys_const.GRAVITY_ACCELERATION

    # 加速度[m/s^2]を計算
    # ネットフォース[N] / 質量[kg] = 加速度[m/s^2]
    if balloon.mass == 0:
        raise ValueError("Balloon mass must not be zero to avoid division by zero.")
    acceleration = net_force / balloon.mass
    acceleration_vector = np.array([0.0, 0.0, acceleration])

    return acceleration_vector
