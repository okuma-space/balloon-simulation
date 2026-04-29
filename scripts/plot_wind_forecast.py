from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from environment.wind import wind_forecast_model


OUTPUT_PATH = Path("docs/images/generated/wind_forecast_velocity_history.png")


def parse_wind_forecast_datetime(
    raw_wind_forecast: list[list],
) -> list[tuple[datetime, float, float, float]]:
    """
    [time, vx, vy, vz] 形式の風速予報リストを,
    calculate_wind_vector() に渡せる形式へ変換する.

    Parameters
    ----------
    raw_wind_forecast : list[list]
        各要素は [time, vx, vy, vz].
        time は ISO8601 文字列.

    Returns
    -------
    list[tuple[datetime, float, float, float]]
        各要素は (time, vx, vy, vz).
    """
    return [
        (
            datetime.fromisoformat(item[0].replace("Z", "+00:00")),
            float(item[1]),
            float(item[2]),
            float(item[3]),
        )
        for item in raw_wind_forecast
    ]


def save_wind_forecast_velocity_history_png(
    time_seconds: np.ndarray,
    wind_velocity_x: np.ndarray,
    wind_velocity_y: np.ndarray,
    output_path: Path,
) -> None:
    """
    風速予報の Vx, Vy 時系列をPNG保存する.

    Parameters
    ----------
    time_seconds : np.ndarray
        開始時刻からの経過秒 [s].
    wind_velocity_x : np.ndarray
        X方向風速 [m/s].
    wind_velocity_y : np.ndarray
        Y方向風速 [m/s].
    output_path : Path
        PNG出力先.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(time_seconds, wind_velocity_x, label="Wind Vx [m/s]")
    ax.plot(time_seconds, wind_velocity_y, linestyle="--", label="Wind Vy [m/s]")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Wind Velocity [m/s]")
    ax.set_title("Wind Forecast Velocity History")
    ax.grid(True)
    ax.legend()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    raw_wind_forecast = [
        ["2026-01-01T00:00:00Z", -0.6, 13.1, 0.0],
        ["2026-01-01T00:15:00Z", -2.3, 11.0, 0.0],
        ["2026-01-01T00:30:00Z", 1.1, 15.4, 0.0],
        ["2026-01-01T00:45:00Z", -1.6, 16.2, 0.0],
        ["2026-01-01T01:00:00Z", -3.0, 13.6, 0.0],
        ["2026-01-01T01:15:00Z", -1.4, 10.5, 0.0],
        ["2026-01-01T01:30:00Z", 0.8, 11.8, 0.0],
        ["2026-01-01T01:45:00Z", 1.6, 14.9, 0.0],
        ["2026-01-01T02:00:00Z", -0.9, 15.2, 0.0],
        ["2026-01-01T02:15:00Z", -1.8, 13.7, 0.0],
        ["2026-01-01T02:30:00Z", -3.4, 12.1, 0.0],
        ["2026-01-01T02:45:00Z", -2.1, 10.9, 0.0],
        ["2026-01-01T03:00:00Z", 0.4, 11.6, 0.0],
        ["2026-01-01T03:15:00Z", 0.2, 13.3, 0.0],
        ["2026-01-01T06:15:00Z", 0.0, 10.0, 0.0],
    ]

    wind_forecast_list = parse_wind_forecast_datetime(raw_wind_forecast)

    start_time = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
    end_time = datetime.fromisoformat("2026-01-01T06:00:00+00:00")
    interval = timedelta(minutes=1)

    time_seconds_list = []
    wind_velocity_x_list = []
    wind_velocity_y_list = []

    current_time = start_time
    while current_time <= end_time:
        wind_vector = wind_forecast_model.calculate_wind_vector(
            wind_forecast_list,
            current_time,
        )

        time_seconds_list.append((current_time - start_time).total_seconds())
        wind_velocity_x_list.append(wind_vector[0])
        wind_velocity_y_list.append(wind_vector[1])

        current_time += interval

    save_wind_forecast_velocity_history_png(
        time_seconds=np.array(time_seconds_list, dtype=float),
        wind_velocity_x=np.array(wind_velocity_x_list, dtype=float),
        wind_velocity_y=np.array(wind_velocity_y_list, dtype=float),
        output_path=OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()