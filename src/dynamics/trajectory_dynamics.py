from models.balloon_model import BalloonModel
import numpy as np
import physics.fluid_mechanics as fluid_mechanics
import phys_const


def calculate_acceleration_vector(
    velocity_vector: np.ndarray,
    balloon_model: BalloonModel,
    out_density: float,
    wind_vector: np.ndarray,
    gas_density: float,
    gas_mass: float,
    balloon_volume: float,
    cross_section_area: float,
) -> np.ndarray:
    """
    気球の加速度ベクトルを計算する.
    外気密度, 気球内ガス密度, 気球体積, 速度ベクトルから,
    浮力・抗力・重力を計算し, 気球の加速度ベクトルを返す.
    本関数では z 軸正方向を上向きとし, 鉛直方向の運動のみを扱う.


    Parameters
    ----------
    velocity_vector : np.ndarray
        気球の速度ベクトル [vx, vy, vz] [m/s].
    balloon_model : BalloonModel
        気球モデル.
        payload_mass, balloon_drag_coefficient などを保持する.
    out_density : float
        外気密度 [kg/m^3].
    wind_vector: np.ndarray,
        風向ベクトル[m/s]
    gas_density : float
        気球内ガス密度 [kg/m^3].
    gas_mass : float
        気球内ガス質量 [kg].
    balloon_volume : float
        気球体積 [m^3].
    cross_section_area : float
        気球の進行方向に対する投影断面積 [m^2].

    Returns
    -------
    np.ndarray
        気球の加速度ベクトル [ax, ay, az] [m/s^2].
    """

    # 加速度[m/s^2]計算する
    # 浮力[N]を計算
    buoyant_force = fluid_mechanics.buoyant_force(
        out_density,
        gas_density,
        balloon_volume,
    )

    # 抗力[N]を計算
    # 風力は一旦0.0[m/s]固定で計算する
    drag_force = fluid_mechanics.drag_force(
        out_density,
        wind_vector,
        velocity_vector,
        balloon_model.balloon_drag_coefficient,
        cross_section_area,
    )

    # 鉛直方向の合力(ネットフォース)[N]を計算する
    # 浮力[N] + 抗力[N] -ペイロード重力[N] = ネットフォース[N]
    net_force_z = (
        buoyant_force
        + drag_force[2]
        - (balloon_model.payload_mass) * phys_const.GRAVITY_ACCELERATION
    )

    # 水平方向と鉛直方向を合成して三次元の加速度[m/s^2]を計算
    # ネットフォース[N] / 質量[kg] = 加速度[m/s^2]
    acceleration_vector = np.array([drag_force[0], drag_force[1], net_force_z]) / (
        balloon_model.payload_mass + gas_mass
    )

    return acceleration_vector
