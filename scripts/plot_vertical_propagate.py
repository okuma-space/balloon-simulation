import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from systems.balloon import Balloon
import dynamics.vertical_dynamics as vertical_dynamics

OUTPUT_DIR = Path("docs")


def simulate_balloon_trajectory(
    balloon: Balloon,
    epoch_time: datetime,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    time_step: timedelta,
    propagation_time: timedelta,
) -> tuple[np.ndarray, np.ndarray]:
    """指定されたpropagation_timeにわたって気球の鉛直ダイナミクスをシミュレートし、時刻と高度の配列を返す。"""
    traj = vertical_dynamics.propagate(
        balloon,
        epoch_time,
        initial_position,
        initial_velocity,
        time_step,
        propagation_time,
    )
    times = np.array([ (t - epoch_time).total_seconds() for t in traj.time_list ])
    positions = np.array(traj.position_vector_list)
    altitude = positions[:, 2]
    return times, altitude


def save_trajectory_html(time_seconds: np.ndarray, altitude: np.ndarray, output_path: Path) -> None:
    """高度と時刻の配列をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_seconds, y=altitude, mode="lines", name="Altitude"))
    fig.update_layout(
        title="Balloon Trajectory",
        xaxis_title="Time [s]",
        yaxis_title="Altitude [m]",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_trajectory_png(time_seconds: np.ndarray, altitude: np.ndarray, output_path: Path) -> None:
    """高度と時刻の配列をプロットしてPNGファイルに保存。"""
    plt.figure()
    plt.plot(time_seconds, altitude)
    plt.title("Balloon Trajectory")
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [m]")
    plt.grid(True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # 気球の初期条件を定義
    balloon = Balloon(
        mass=1.0,  # [kg]
        gas_density=0.178,  # [kg/m^3] (ヘリウムの密度)　(https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
        volume=1.0,  # [m^3]
    )

    # 初期位置と速度を定義
    epoch = datetime(2026, 1, 1, 0, 0, 0)
    initial_position = np.array([0.0, 0.0, 0.0])
    initial_velocity = np.array([0.0, 0.0, 0.0])

    # 伝播時間とタイムステップを定義
    time_step = timedelta(seconds=1)
    propagation_duration = timedelta(seconds=3600)

    # シミュレーションを実行して時刻と高度の配列を取得
    time_seconds, altitude = simulate_balloon_trajectory(
        balloon,
        epoch,
        initial_position,
        initial_velocity,
        time_step,
        propagation_duration,
    )

    html_path = OUTPUT_DIR / "html/balloon_trajectory.html"
    png_path = OUTPUT_DIR / "png/balloon_trajectory.png"

    # HTMLとPNGを保存
    save_trajectory_html(time_seconds, altitude, html_path)
    save_trajectory_png(time_seconds, altitude, png_path)

    print(f"saved: {html_path}")
    print(f"saved: {png_path}")


if __name__ == "__main__":
    main()