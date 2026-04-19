from systems.balloon_system import BalloonSystem
import numpy as np
import physics.balloon_mechanics as balloon_mechanics
from systems.balloon_state_history import BalloonStateHistory
from datetime import datetime, timedelta
from dynamics import propagate_trajectory
from dynamics import propagate_state


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
    # trajectory
    time_list = [epoch_time]
    position_vector_list = [initial_position.copy()]
    velocity_vector_list = [initial_velocity.copy()]

    # state
    gas_mass_list = [balloon.initial_gas_mass]  # 初期値設定
    volume_list = [balloon.ground_volume]  # 初期体積[m^3]は地表面上での体積とする
    cross_sectional_area_list = [
        balloon_mechanics.sphere_cross_section_area(volume_list[0])
    ]  # 初期断面積[m^2]を計算して保存
    gas_density_list = [
        gas_mass_list[0] / volume_list[0]
    ]  # 初期ガス密度[kg/m^3]を計算して保存
    gas_temperature_list = [balloon.initial_gas_temperature]  # 初期ガス温度を取得する

    # propagatorの初期化
    current_time = epoch_time
    end_time = epoch_time + propagation_time
    time_step_seconds = time_step.total_seconds()  # タイムステップを秒に変換
    save_interval_steps = int(
        save_state_interval.total_seconds() / time_step_seconds
    )  # 状態保存のインターバルをステップ数に変換

    # propagationループ
    while current_time < end_time:
        # ルンゲクッタ法で位置と速度を伝搬更新する
        position, velocity = propagate_trajectory.propagate_trajectory(
            balloon,
            position_vector_list[-1],
            velocity_vector_list[-1],
            gas_mass_list[-1],
            volume_list[-1],
            cross_sectional_area_list[-1],
            gas_density_list[-1],
            current_time,
            time_step_seconds,
        )

        # stateを伝搬更新する
        gas_mass, volume, cross_sectional_area, gas_density, gas_temperature = (
            propagate_state.propagate_state(
                balloon,
                current_time,
                position,
                velocity,
                gas_mass_list,
                volume_list,
                cross_sectional_area_list,
                gas_density_list,
                gas_temperature_list,
                time_step_seconds,
            )
        )

        # 時刻を保存
        current_time += time_step

        # 更新されたtrajectoryを保存
        time_list.append(current_time)
        position_vector_list.append(position)
        velocity_vector_list.append(velocity)

        # 更新されたstateを保存
        gas_mass_list.append(gas_mass)
        volume_list.append(volume)
        cross_sectional_area_list.append(cross_sectional_area)
        gas_density_list.append(gas_density)
        gas_temperature_list.append(gas_temperature)

    # 容量削減のためにデータを間引く
    if save_interval_steps > 1:
        time_list = time_list[::save_interval_steps]
        position_vector_list = position_vector_list[::save_interval_steps]
        velocity_vector_list = velocity_vector_list[::save_interval_steps]
        volume_list = volume_list[::save_interval_steps]
        gas_density_list = gas_density_list[::save_interval_steps]
        gas_mass_list = gas_mass_list[::save_interval_steps]
        gas_temperature_list = gas_temperature_list[::save_interval_steps]
        cross_sectional_area_list = cross_sectional_area_list[::save_interval_steps]

    # BalloonStateHistoryオブジェクトを作成して返す
    return BalloonStateHistory(
        time_list,
        position_vector_list,
        velocity_vector_list,
        volume_list,
        gas_density_list,
        gas_mass_list,
        gas_temperature_list,
        cross_sectional_area_list,
    )
