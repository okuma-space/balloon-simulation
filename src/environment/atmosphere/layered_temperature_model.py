def calculate_temperature(altitude: float) -> float:
    """
    高度に応じた大気温度を計算する分層大気温度モデル.
    宇宙システム入門 P.7の図1.1及び1976 Standard Atmosphere Tableを元に,レイヤ毎に線形と一定値で計算をする.
    https://www.pdas.com/atmosTable1SI.html

    Parameters
    ----------
    altitude : float
        高度 [m]

    Returns
    -------
    tempulature : float
        大気温度 [K]
    """
    if altitude < 12000.0:
        # 1層(0~12[km])
        # 288.1[K]から216.6[K]までの線形補間
        temperature = 288.1 + (216.6 - 288.1) * altitude / 12000.0
    elif altitude < 20000.0:
        # 2層(12~20[km])
        # 216.6[K]一定
        temperature = 216.6

    elif altitude < 35000.0:
        # 3層(20~35[km])
        # 216.6[K]から235[K]までの線形補間
        temperature = 216.6 + (235.0 - 216.6) * (altitude - 20000.0) / 15000.0

    elif altitude < 50000.0:
        # 4層(35~50[km])
        # 235[K]から270[K]までの線形補間
        temperature = 235.0 + (270.0 - 235.0) * (altitude - 35000.0) / 15000.0

    else:
        # 5層 (>50 km)
        # 270[K]一定(将来的にはここも線形補間とする)
        temperature = 270.0

    return temperature
