from datetime import datetime
import numpy as np


def calculate_wind_vector(
    wind_forecast: list[tuple[datetime, float, float, float]],
    target_time: datetime,
) -> np.ndarray:
    """
    指定時刻における風速ベクトルを線形補間で計算する.

    Parameters
    ----------
    wind_forecast : list[tuple[datetime, float, float, float]]
        風速予報データ.
        各要素は (time, vx, vy, vz) の形式とする.
        time は datetime, vx/vy/vz は風速成分 [m/s].
    target_time : datetime
        補間対象の時刻.

    Returns
    -------
    np.ndarray
        補間された風速ベクトル [vx, vy, vz] [m/s].

    Notes
    -----
    target_time が予報範囲外の場合は, 端点の風速をそのまま返す.
    """
    if len(wind_forecast) == 0:
        raise ValueError("wind_forecast must not be empty.")

    sorted_forecast = sorted(wind_forecast, key=lambda item: item[0])

    # 範囲外なら端点を返す
    first_time, first_vx, first_vy, first_vz = sorted_forecast[0]
    if target_time <= first_time:
        return np.array([first_vx, first_vy, first_vz], dtype=float)

    last_time, last_vx, last_vy, last_vz = sorted_forecast[-1]
    if target_time >= last_time:
        return np.array([last_vx, last_vy, last_vz], dtype=float)

    # 範囲内なら線形補間
    for i in range(len(sorted_forecast) - 1):
        time0, vx0, vy0, vz0 = sorted_forecast[i]
        time1, vx1, vy1, vz1 = sorted_forecast[i + 1]

        if time0 <= target_time <= time1:
            total_seconds = (time1 - time0).total_seconds()
            elapsed_seconds = (target_time - time0).total_seconds()

            if total_seconds <= 0.0:
                raise ValueError("wind_forecast contains duplicate or invalid times.")

            ratio = elapsed_seconds / total_seconds

            wind0 = np.array([vx0, vy0, vz0], dtype=float)
            wind1 = np.array([vx1, vy1, vz1], dtype=float)

            return (1.0 - ratio) * wind0 + ratio * wind1

    raise RuntimeError("Unexpected wind interpolation state.")
