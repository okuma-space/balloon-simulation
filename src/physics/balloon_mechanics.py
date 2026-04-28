import numpy as np
import environment.atmosphere.isothermal_model as isothermal_model
import phys_const
from models.gas import LiftingGasType
from models.balloon_model import BalloonModel
from physics import fluid_mechanics


def calculate_ground_volume(altitude: float, target_volume: float) -> float:
    """
    指定した高度で指定した体積となる気球の地表面上での体積を求める。

    Parameters
    ----------
    altitude : float
        高度 [m]
    target_volume : float
        指定した高度での体積 [m^3]

    Returns
    -------
    float
        地表面上での体積 [m^3]
    """
    # 指定した高度での大気密度を計算
    air_density_at_altitude = isothermal_model.calculate_density(altitude)

    # 指定した高度での大気圧を計算
    air_pressure_at_altitude = isothermal_model.calculate_pressure(
        air_density_at_altitude
    )

    # 地表面上での大気密度を計算
    air_density_at_ground = isothermal_model.calculate_density(0.0)

    # 地表面での大気圧を計算
    air_pressure_at_ground = isothermal_model.calculate_pressure(air_density_at_ground)

    # 地表体積の計算（ボイル則）
    ground_volume = target_volume * air_pressure_at_altitude / air_pressure_at_ground
    return ground_volume


def calculate_volume_at_altitude(
    out_pressure: float,
    gas_temperature: float,
    gas_mass: float,
    gas_type: LiftingGasType,
    max_volume: float,
) -> float:
    """
    理想気体の状態方程式から気球体積を計算する。

    外部圧力、ガス温度、ガス質量から PV = nRT の関係式を用いて
    V = mRT/P により体積を算出する.
    計算結果が最大体積を超える場合は最大体積で制限される.

    Parameters
    ----------
    out_pressure : float
        気球外部圧力 [Pa]
    gas_temperature : float
        ガス温度 [K]
    gas_mass : float
        現在のガス質量 [kg]
    gas_type : LiftingGasType
        揚力ガスの種類（HELIUM または HYDROGEN）
    max_volume : float
        気球の最大体積 [m^3]

    Returns
    -------
    float
        気球体積 [m^3]（最大体積を超える場合は max_volume）
    """
    # ガスタイプから気体ガス定数を取得
    if gas_type == LiftingGasType.HELIUM:
        specific_gas_constant = phys_const.HELIUM_SPECIFIC_GAS_CONSTANT
    elif gas_type == LiftingGasType.HYDROGEN:
        specific_gas_constant = phys_const.HYDROGEN_SPECIFIC_GAS_CONSTANT
    else:
        raise ValueError(f"Unsupported gas type: {gas_type}")

    # 体積[m^3] = ガス質量[kg] *  比気体定数[J/(kg·K)] * 温度[K] / 外気圧[Pa]
    volume = gas_mass * specific_gas_constant * gas_temperature / out_pressure

    # 最大体積を超える場合は最大体積で制限
    return min(volume, max_volume)


def sphere_cross_section_area(volume) -> float:
    """
    球体の断面積[m^2]を計算する

    Parameters
    ----------
    volume : float
        体積 [m^3]

    Returns
    -------
    float
        球体の断面積 m^2]
    """

    # 気球の体積がマイナス以下もしくは非数値なら断面積を0とする
    if not np.isfinite(volume) or volume <= 0.0:
        return 0.0

    # 体積V[m^3]から半径r[m]を求める式
    # V = (4/3) * π * r^3  =>  r = (3V / (4π))^(1/3)
    r = (3 * volume / (4 * np.pi)) ** (1 / 3)

    # 断面積[m^2]を計算して返す
    # πr^2
    return np.pi * r**2


def calculate_balloon_pressure(
    temperature: float,
    gas_mass: float,
    volume: float,
    gas_type: LiftingGasType,
) -> float:
    """
    気球内部の圧力を計算する関数.
    理想気体の状態方程式を用いる.
    PV = mRT
    P = mRT / V

    Parameters
    ----------
    temperature : float
        ガス温度 [K]
    gas_mass : float
        ガス質量 [kg]
    volume : float
        気球体積 [m^3]
    gas_type : LiftingGasType
        揚力ガスの種類

    Returns
    -------
    float
        気球内部圧力 [Pa]
    """
    # 引数validate(温度,質量,体積)
    if temperature <= 0.0:
        raise ValueError("temperature must be positive")

    # 質量もしくは体積0.0以下はガスを放出しきった状態を示すので、0で返す
    if gas_mass < 0.0 or volume <= 0.0:
        return 0.0

    # ガスタイプから気体ガス定数を取得
    if gas_type == LiftingGasType.HELIUM:
        specific_gas_constant = phys_const.HELIUM_SPECIFIC_GAS_CONSTANT
    elif gas_type == LiftingGasType.HYDROGEN:
        specific_gas_constant = phys_const.HYDROGEN_SPECIFIC_GAS_CONSTANT
    else:
        raise ValueError(f"Unsupported gas type: {gas_type}")

    # 理想気体の状態方程式から計算
    # 内部圧力[Pa] = ガス質量[kg] * 比気体定数[J/(kg·K)] * 温度[K] / 体積[m^3]
    pressure = gas_mass * specific_gas_constant * temperature / volume
    return pressure


def calculate_temperature(out_temperature: float, gas_temperature: float) -> float:
    """
    気球ガスの温度を計算する.

    外部温度と現在のガス温度から,気球内のガス温度を更新する.
    計算式は簡易的に (out_temperature - gas_temperature) / 1000.0 + gas_temperature を用いる.

    Parameters
    ----------
    out_temperature : float
        外部温度 [K]
    gas_temperature : float
        現在のガス温度 [K]

    Returns
    -------
    float
        更新後のガス温度 [K]
    """
    delta_gas_temperature = (out_temperature - gas_temperature) / 2000.0
    return delta_gas_temperature


def calculate_derived_state_variables(
    gas_temperature: float,
    gas_mass: float,
    position_vector: np.ndarray,
    balloon_model: BalloonModel,
    out_pressure: float | None = None,
):
    """
    気球の独立状態変数から従属状態変数を計算する.
    ----------
    gas_temperature : .float
        ガス温度[K]
    gas_mass :  float
        ガス質量[Kg]
    position_vector :  np.ndarray
        位置ベクトル[m]
    balloon_model : BalloonModel
        気球モデル
    out_pressure : float
        外気圧[Pa](省略可)
    Returns
    -------
    np.ndarray
        従属状態変数
        [0] = 気球体積[m^3],
        [1] = 気球断面積[m^2],
        [2] = ガス密度[kg/m^3]
    """

    # 外気圧が与えられない時は計算する
    if out_pressure is None:
        altitude = position_vector[2]
        # 外気密度[kg/m^3]
        out_density = isothermal_model.calculate_density(altitude)

        # 外気圧[Pa]
        out_pressure = isothermal_model.calculate_pressure(out_density)

    # 体積[m^3]
    balloon_volume = calculate_volume_at_altitude(
        out_pressure,
        gas_temperature,
        gas_mass,
        balloon_model.gas_type,
        balloon_model.max_volume,
    )

    # 断面積[m^2]
    # ペイロード断面積が気球断面積を上回る場合はペイロード断面積を用いる
    cross_sectional_area = sphere_cross_section_area(balloon_volume)
    cross_sectional_area = max(cross_sectional_area, balloon_model.payload_area)

    # ガス密度[kg/m^3]
    gas_density = fluid_mechanics.calculate_density(gas_mass, balloon_volume)

    return np.array(
        [
            balloon_volume,
            cross_sectional_area,
            gas_density,
        ],
        dtype=float,
    )
