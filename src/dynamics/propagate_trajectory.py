from systems.balloon_system import BalloonSystem
import environment.atmosphere.isothermal_model as isothermal_model
import numpy as np
import physics.fluid_mechanics as fluid_mechanics
import phys_const
import numerics.runge_kutta as runge_kutta
from datetime import datetime, timedelta


def propagate_trajectory(
    balloon,
    position_vector,
    velocity_vector,
    gas_mass,
    volume,
    cross_sectional_area,
    gas_density,
    current_time,
    time_step_seconds,
):
    """
    ルンゲクッタ法を用いて,気球の位置と速度を更新する関数.
    Parameters
    ----------
    balloon : BalloonSystem
        気球オブジェクト
    position_vector : np.ndarray
        位置ベクトル [x, y, z] [m]
    velocity_vector : np.ndarray
        速度ベクトル [vx, vy, vz] [m/s]
    gas_mass : float
        ガス質量 [kg]
    volume : float
        気球の体積 [m^3]
    cross_sectional_area : float
        気球の断面積 [m^2]
    gas_density : float
        気球内のガス密度 [kg/m^3]
    time_step_seconds : float
        タイムステップ [s]

    Returns
    -------
    position : np.ndarray
        更新された位置ベクトル [x, y, z] [m]
    velocity : np.ndarray
        更新された速度ベクトル [vx, vy, vz] [m/s]
    """

    # 状態ベクトルは [position, velocity]
    state_vector = np.hstack((position_vector, velocity_vector))

    # ルンゲクッタ法で状態ベクトルを更新する
    state_vector = runge_kutta.rk4_step(
        calculate_trajectory_derivative,
        t=0.0,  # ルンゲクッタ法の中で使用される時刻は、現在の時刻からの相対的な時間であるため、0.0を渡す
        y=state_vector,
        dt=time_step_seconds,
        balloon=balloon,
        gas_mass=gas_mass,
        volume=volume,
        cross_sectional_area=cross_sectional_area,
        gas_density=gas_density,
        current_time=current_time,  # ルンゲクッタ法の中で使用される時刻は、現在の時刻からの相対的な時間であるため、current_timeを渡す必要はないが、将来的に環境モデルの時間変化を考慮する際に使用する可能性があるため、引数として渡すようにしている
    )

    # 更新された状態ベクトルから位置と速度を抽出
    position = state_vector[0:3]
    velocity = state_vector[3:6]

    # 地表面衝突判定
    if position[2] < 0.0:
        position = np.array([position[0], position[1], 0.0])
        velocity = np.array([0.0, 0.0, 0.0])
        return position, velocity

    # 更新された位置と速度を返す
    return position, velocity


def calculate_trajectory_derivative(
    relative_time: float,
    state_vector: np.ndarray,
    balloon,
    gas_mass: float,
    volume: float,
    cross_sectional_area: float,
    gas_density: float,
    current_time: datetime,
) -> np.ndarray:
    """
    状態ベクトル(位置と速度)の時間微分を計算する関数.
    ルンゲクッタ法の中で呼び出されることを想定しており、追加の引数として気球のプロパティや環境条件を受け取る.
    Parameters
    ----------
    relative_time : float
        ルンゲクッタ法の中で使用される相対時刻 [s]
    state_vector : np.ndarray
        状態ベクトル.
        ここではposition[m], velocity[m/s]を含む6次元のベクトルを想定している.
        [position_x, position_y, position_z, velocity_x, velocity_y, velocity_z]
    balloon : BalloonSystem
        気球オブジェクト.
    volume : float
        気球の体積 [m^3]
    cross_sectional_area : float
        気球の断面積 [m^2]
    gas_density : float
        気球内のガス密度 [kg/m^3]
    current_time : datetime
        現在の時刻[UTC]
        未使用の引数だが、将来的に環境モデルの時間変化を考慮する際に使用する可能性があるため、引数として受け取るようにしている.
        例 太陽位置など

    Returns
    -------
    np.ndarray
        状態ベクトルの時間微分 [velocity, acceleration]
    """
    # 現在の時刻を計算.
    # 絶対時刻にルンゲクッタ計算内部での相対時刻を加算する.
    # 将来実装のため現時点ではruffを無効化する
    absolute_time = current_time + timedelta(seconds=relative_time)  # noqa: F841

    # 状態ベクトルから位置と速度を抽出
    position = state_vector[0:3]
    velocity = state_vector[3:6]

    # 加速度[m/s^2]の計算
    acceleration = calculate_vertical_acceleration(
        balloon,
        position,
        velocity,
        gas_mass,
        volume,
        cross_sectional_area,
        gas_density,
    )

    # 状態ベクトルの時間微分は [velocity, acceleration]
    return np.hstack((velocity, acceleration))


def calculate_vertical_acceleration(
    balloon: BalloonSystem,
    position_vector: np.ndarray,
    velocity_vector: np.ndarray,
    gas_mass: float,
    volume: float,
    cross_sectional_area: float,
    gas_density: float,
) -> np.ndarray:
    """
    気球の浮力と重力に基づいて気球の鉛直加速度を計算する。

    Parameters
    ----------
    balloon : BalloonSystem
        気球オブジェクト.
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
    buoyant_force = fluid_mechanics.buoyant_force(air_density, gas_density, volume)

    # 抗力[N]を計算
    # 風力は一旦0.0[m/s]固定で計算する
    drag_force = fluid_mechanics.drag_force(
        air_density,
        [0.0, 0.0, 0.0],
        velocity_vector,
        balloon.balloon_drag_coefficient,
        cross_sectional_area,
    )[2]  # 鉛直方向の抗力のみを考慮

    # 合力(ネットフォース)[N]を計算する
    # 浮力[N] + 抗力[N] -重力[N] = ネットフォース[N]
    net_force = (
        buoyant_force
        + drag_force
        - (balloon.payload_mass + gas_mass) * phys_const.GRAVITY_ACCELERATION
    )

    # 加速度[m/s^2]を計算
    # ネットフォース[N] / 質量[kg] = 加速度[m/s^2]
    if balloon.payload_mass + gas_mass == 0:
        raise ValueError("Total mass must not be zero to avoid division by zero.")
    acceleration = net_force / (balloon.payload_mass + gas_mass)
    acceleration_vector = np.array([0.0, 0.0, acceleration])

    return acceleration_vector
