import math
import phys_const


# 等温大気モデルとしての環境パラメタ
CONSTANT_TEMPERATURE_SEA_LEVEL = 288.15  # 一定温度[K]として海面温度を採用 (https://en.wikipedia.org/wiki/International_Standard_Atmosphere)
CONSTANT_AIR_MOLAR_MASS = 0.0289644  # 一定の空気の分子量質量[kg/mol]として乾燥空気のモル質量を採用 (https://en.wikipedia.org/wiki/Density_of_air)
AIR_DENSITY_SEA_LEVEL = 1.225  # 基準高度での大気密度[kg/m^3]として海面での大気密度を採用 (https://en.wikipedia.org/wiki/International_Standard_Atmosphere)

# scale height(H)の計算 (宇宙システム入門 P.52 (3.23))
SCALE_HEIGHT = (
    phys_const.GAS_CONSTANT
    * CONSTANT_TEMPERATURE_SEA_LEVEL
    / (CONSTANT_AIR_MOLAR_MASS * phys_const.GRAVITY_ACCELERATION)
)


def calculate_density(altitude: float) -> float:
    """
    高度に応じた大気密度を計算する等温大気モデル
    等温大気モデルにおいては重力加速度、空気の分子量質量、大気温度は高度に依存しない一定値と仮定される。 (宇宙システム入門 P.51)
    reference: https://glossary.ametsoc.org/wiki/isothermal-atmosphere/

    Parameters
    ----------  altitude : float
        高度 [m]
    Returns
    -------  density : float
        大気密度 [kg/m^3]
    """

    # 大気密度[kg/m^3] (宇宙システム入門 P.52 (3.24))
    density = AIR_DENSITY_SEA_LEVEL * math.exp(-altitude / SCALE_HEIGHT)

    return density
