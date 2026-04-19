from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("docs")


def save_position_trajectory_html(
    time_seconds: np.ndarray,
    altitude: np.ndarray,
    velocity: np.ndarray,
    output_path: Path,
) -> None:
    """高度と速度と時刻の配列をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()

    # 高度（左軸）
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=altitude,
            mode="lines",
            name="Altitude [m]",
            yaxis="y1",
            hovertemplate="Time: %{x:.1f}<br>Altitude: %{y:.1f} m",
        )
    )

    # 速度（右軸）
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=velocity,
            mode="lines",
            name="Vertical Velocity [m/s]",
            yaxis="y2",
            hovertemplate="Time: %{x:.1f}<br>Velocity: %{y:.1f} m/s",
        )
    )

    fig.update_layout(
        title="Balloon Position and Velocity Trajectory",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(
            title="Altitude [m]",
            side="left",
        ),
        yaxis2=dict(
            title="Velocity [m/s]",
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_trajectory_png(
    time_seconds: np.ndarray,
    altitude: np.ndarray,
    velocity: np.ndarray,
    output_path: Path,
) -> None:
    """高度・速度と時刻の配列をプロットしてPNGファイルに保存。"""
    fig, ax1 = plt.subplots()

    # altitude（左軸）
    ax1.plot(time_seconds, altitude, label="Altitude [m]")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Altitude [m]")
    ax1.grid(True)

    # velocity（右軸）
    ax2 = ax1.twinx()
    ax2.plot(time_seconds, velocity, linestyle="--", label="Vertical Velocity [m/s]")
    ax2.set_ylabel("Velocity [m/s]")

    # 凡例統合
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        fontsize=6,
        frameon=True,
        framealpha=0.8,
        labelspacing=0.2,
        handlelength=1.0,
        handletextpad=0.3,
        borderpad=0.2,
    )

    plt.title("Balloon Position and Velocity Trajectory")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
