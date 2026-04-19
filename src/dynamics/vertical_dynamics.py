import systems.balloon_system as BalloonSystem
import environment.atmosphere.isothermal_model as isothermal_model
import numpy as np
import physics.fluid_mechanics as fluid_mechanics
import physics.balloon_mechanics as balloon_mechanics
import phys_const
from systems.balloon_state_history import BalloonStateHistory
from datetime import datetime, timedelta


def propagate(
    balloon: BalloonSystem,
    epoch_time: datetime,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    time_step: timedelta,
    save_state_interval: timedelta,
    propagation_time: timedelta,
) -> BalloonStateHistory:
    """
    指定された propagation_time にわたって気球の鉛直ダイナミクスをシミュレートする

    Parameters
    ----------
    balloon : BalloonSystem
        気球のプロパティを含む気球オブジェクト
    epoch_time : datetime
        propagator の開始時刻
    initial_position : np.ndarray
        初期位置ベクトル [x, y, z] [m]
    initial_velocity : np.ndarray
        初期速度ベクトル [vx, vy, vz] [m/s]
    time_step : timedelta
        propagator 反復のタイムステップ
    save_state_interval : timedelta
        状態保存のインターバル
    propagation_time : timedelta
        propagator の総時間

    Returns
    -------
    BalloonStateHistory
        気球のstateを記録したHistory オブジェクト
    """

    # balloon state historyの初期化
    time_list = [epoch_time]
    position_vector_list = [initial_position.copy()]
    velocity_vector_list = [initial_velocity.copy()]
    volume_list = [balloon.ground_volume]  # 初期体積[m^3]は地表面上での体積とする
    cross_sectional_area_list = [
        balloon_mechanics.sphere_cross_section_area(volume_list[0])
    ]  # 初期断面積[m^2]を計算して保存
    gas_density_list = [
        fluid_mechanics.calculate_density(balloon.gas_mass, volume_list[0])
    ]  # 初期ガス密度[kg/m^3]を計算して保存

    # propagatorの初期化
    current_time = epoch_time
    end_time = epoch_time + propagation_time
    time_step_seconds = time_step.total_seconds()  # タイムステップを秒に変換
    save_interval_steps = int(
        save_state_interval.total_seconds() / time_step_seconds
    )  # 状態保存のインターバルをステップ数に変換

    # propagationループ
    while current_time < end_time:
        # 加速度[m/s^2]の計算
        acceleration = calculate_vertical_acceleration(
            balloon,
            position_vector_list[-1],
            velocity_vector_list[-1],
            volume_list[-1],
            cross_sectional_area_list[-1],
            gas_density_list[-1],
        )

        # 簡単なオイラー法で位置と速度を更新する
        velocity = velocity_vector_list[-1] + acceleration * time_step_seconds
        position = position_vector_list[-1] + velocity * time_step_seconds

        # 体積[m^3]を更新
        current_time_volume = balloon_mechanics.calculate_volume_at_altitude(
            position[2], balloon.ground_volume
        )
        if current_time_volume > balloon.max_volume:
            current_time_volume = balloon.max_volume  # 体積の上限を設定

        # 断面積[m^2]の更新
        current_time_cross_sectional_area = balloon_mechanics.sphere_cross_section_area(
            current_time_volume
        )

        # ガス密度[kg/m^3]の更新
        current_time_gas_density = fluid_mechanics.calculate_density(
            balloon.gas_mass, current_time_volume
        )

        # 時刻を保存
        current_time += time_step

        # 更新されたtrajectoryを保存
        time_list.append(current_time)
        position_vector_list.append(position)
        velocity_vector_list.append(velocity)
        # 更新されたstateを保存
        volume_list.append(current_time_volume)
        cross_sectional_area_list.append(current_time_cross_sectional_area)
        gas_density_list.append(current_time_gas_density)

    # 容量削減のためにデータを間引く
    if save_interval_steps > 1:
        time_list = time_list[::save_interval_steps]
        position_vector_list = position_vector_list[::save_interval_steps]
        velocity_vector_list = velocity_vector_list[::save_interval_steps]
        volume_list = volume_list[::save_interval_steps]
        cross_sectional_area_list = cross_sectional_area_list[::save_interval_steps]
        gas_density_list = gas_density_list[::save_interval_steps]

    # BalloonStateHistoryオブジェクトを作成して返す
    return BalloonStateHistory(
        time_list,
        position_vector_list,
        velocity_vector_list,
        volume_list,
        gas_density_list,
        cross_sectional_area_list,
    )


def calculate_vertical_acceleration(
    balloon: BalloonSystem,
    position_vector: np.ndarray,
    velocity_vector: np.ndarray,
    volume: float,
    cross_sectional_area: float,
    gas_density: float,
) -> np.ndarray:
    """
    気球の浮力と重力に基づいて気球の鉛直加速度を計算する。

    Parameters
    ----------
    balloon : BalloonSystem
        気球オブジェクト。
    position_vector : np.ndarray
        位置ベクトル [x, y, z] [m]
    velocity_vector : np.ndarray
        速度ベクトル [vx, vy, vz] [m/s]
    volume : float
        気球の体積 [m^3]
    cross_sectional_area : float
        気球の断面積 [m^2]
    gas_density : float
        気球内のガス密度 [kg/m^3]

    Returns
    -------
    np.ndarray
        加速度ベクトル [ax, ay, az] [m/s^2]
    """

    # 大気密度[kg/m^3]を計算
    altitude = position_vector[2]  # 高度[m]
    air_density = isothermal_model.calculate_density(altitude)

    # 浮力[N]を計算
    # import pdb; pdb.set_trace()
    buoyant_force = fluid_mechanics.buoyant_force(air_density, gas_density, volume)

    # 抗力[N]を計算
    # 風力は一旦0.0[m/s]固定で計算する
    drag_force = fluid_mechanics.drag_force(
        air_density,
        [0.0, 0.0, 0.0],
        velocity_vector,
        balloon.drag_coefficient,
        cross_sectional_area,
    )[2]  # 鉛直方向の抗力のみを考慮
    # import pdb; pdb.set_trace()

    # 合力(ネットフォース)[N]を計算する
    # 浮力[N] + 抗力[N] -重力[N] = ネットフォース[N]
    net_force = (
        buoyant_force
        + drag_force
        - (balloon.payload_mass + balloon.gas_mass) * phys_const.GRAVITY_ACCELERATION
    )

    # 加速度[m/s^2]を計算
    # ネットフォース[N] / 質量[kg] = 加速度[m/s^2]
    if balloon.payload_mass + balloon.gas_mass == 0:
        raise ValueError("Total mass must not be zero to avoid division by zero.")
    acceleration = net_force / (balloon.payload_mass + balloon.gas_mass)
    acceleration_vector = np.array([0.0, 0.0, acceleration])

    return acceleration_vector
