from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

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


def save_xy_position_trajectory_png(
    position_x: np.ndarray,
    position_y: np.ndarray,
    output_path: Path,
) -> None:
    """X-Y 平面上の位置軌跡をプロットしてPNGファイルに保存。"""
    position_x = np.asarray(position_x, dtype=float)
    position_y = np.asarray(position_y, dtype=float)

    fig, ax = plt.subplots()

    ax.plot(
        position_x,
        position_y,
        marker=".",
        markersize=2,
        label="X-Y Position Trajectory",
    )
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_title("Balloon X-Y Position Trajectory")
    ax.grid(True)

    # yが全部0などの場合、equalだと潰れて見えやすいので一旦切る
    # ax.axis("equal")

    ax.legend()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_xy_velocity_trajectory_png(
    velocity_x: np.ndarray,
    velocity_y: np.ndarray,
    output_path: Path,
) -> None:
    """Vx-Vy 平面上の速度軌跡をプロットしてPNGファイルに保存。"""
    velocity_x = np.asarray(velocity_x, dtype=float)
    velocity_y = np.asarray(velocity_y, dtype=float)

    fig, ax = plt.subplots()

    ax.plot(
        velocity_x,
        velocity_y,
        marker=".",
        markersize=2,
        label="Vx-Vy Velocity Trajectory",
    )
    ax.set_xlabel("Vx [m/s]")
    ax.set_ylabel("Vy [m/s]")
    ax.set_title("Balloon Vx-Vy Velocity Trajectory")
    ax.grid(True)

    # yが全部0などの場合、equalだと潰れて見えやすいので一旦切る
    # ax.axis("equal")

    ax.legend()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_xy_position_trajectory_html(
    position_x: np.ndarray,
    position_y: np.ndarray,
    output_path: Path,
) -> None:
    """X-Y 平面上の位置軌跡をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=position_x,
            y=position_y,
            mode="lines",
            name="X-Y Position Trajectory",
            hovertemplate="X: %{x:.1f} m<br>Y: %{y:.1f} m",
        )
    )

    fig.update_layout(
        title="Balloon X-Y Position Trajectory",
        xaxis=dict(title="X [m]"),
        yaxis=dict(
            title="Y [m]",
            scaleanchor="x",
            scaleratio=1,
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_xy_velocity_trajectory_html(
    velocity_x: np.ndarray,
    velocity_y: np.ndarray,
    output_path: Path,
) -> None:
    """Vx-Vy 平面上の速度軌跡をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=velocity_x,
            y=velocity_y,
            mode="lines",
            name="Vx-Vy Velocity Trajectory",
            hovertemplate="Vx: %{x:.3f} m/s<br>Vy: %{y:.3f} m/s",
        )
    )

    fig.update_layout(
        title="Balloon Vx-Vy Velocity Trajectory",
        xaxis=dict(title="Vx [m/s]"),
        yaxis=dict(
            title="Vy [m/s]",
            scaleanchor="x",
            scaleratio=1,
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_horizontal_position_velocity_png(
    time_seconds: np.ndarray,
    position_x: np.ndarray,
    position_y: np.ndarray,
    velocity_x: np.ndarray,
    velocity_y: np.ndarray,
    output_path: Path,
) -> None:
    """X/Vx と Y/Vy の時系列を1枚のPNGに保存する。"""
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # X position / Vx
    ax_x = axes[0]
    ax_vx = ax_x.twinx()

    ax_x.plot(time_seconds, position_x, label="X [m]")
    ax_vx.plot(
        time_seconds,
        velocity_x,
        linestyle="--",
        label="Vx [m/s]",
    )

    ax_x.set_ylabel("X [m]")
    ax_vx.set_ylabel("Vx [m/s]")
    ax_x.set_title("Balloon X Position and X Velocity History")
    ax_x.grid(True)

    lines_x, labels_x = ax_x.get_legend_handles_labels()
    lines_vx, labels_vx = ax_vx.get_legend_handles_labels()
    ax_x.legend(
        lines_x + lines_vx,
        labels_x + labels_vx,
        loc="upper left",
    )

    # Y position / Vy
    ax_y = axes[1]
    ax_vy = ax_y.twinx()

    ax_y.plot(time_seconds, position_y, label="Y [m]")
    ax_vy.plot(
        time_seconds,
        velocity_y,
        linestyle="--",
        label="Vy [m/s]",
    )

    ax_y.set_xlabel("Time [s]")
    ax_y.set_ylabel("Y [m]")
    ax_vy.set_ylabel("Vy [m/s]")
    ax_y.set_title("Balloon Y Position and Y Velocity History")
    ax_y.grid(True)

    lines_y, labels_y = ax_y.get_legend_handles_labels()
    lines_vy, labels_vy = ax_vy.get_legend_handles_labels()
    ax_y.legend(
        lines_y + lines_vy,
        labels_y + labels_vy,
        loc="upper left",
    )

    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_horizontal_position_velocity_html(
    time_seconds: np.ndarray,
    position_x: np.ndarray,
    position_y: np.ndarray,
    velocity_x: np.ndarray,
    velocity_y: np.ndarray,
    output_path: Path,
) -> None:
    """X/Vx と Y/Vy の時系列を1つのHTMLファイルに保存する。"""
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
        ],
        subplot_titles=(
            "Balloon X Position and X Velocity History",
            "Balloon Y Position and Y Velocity History",
        ),
    )

    # X position
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=position_x,
            mode="lines",
            name="X [m]",
            hovertemplate="Time: %{x:.1f} s<br>X: %{y:.1f} m",
        ),
        row=1,
        col=1,
        secondary_y=False,
    )

    # Vx
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=velocity_x,
            mode="lines",
            name="Vx [m/s]",
            line=dict(dash="dash"),
            hovertemplate="Time: %{x:.1f} s<br>Vx: %{y:.3f} m/s",
        ),
        row=1,
        col=1,
        secondary_y=True,
    )

    # Y position
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=position_y,
            mode="lines",
            name="Y [m]",
            hovertemplate="Time: %{x:.1f} s<br>Y: %{y:.1f} m",
        ),
        row=2,
        col=1,
        secondary_y=False,
    )

    # Vy
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=velocity_y,
            mode="lines",
            name="Vy [m/s]",
            line=dict(dash="dash"),
            hovertemplate="Time: %{x:.1f} s<br>Vy: %{y:.3f} m/s",
        ),
        row=2,
        col=1,
        secondary_y=True,
    )

    fig.update_xaxes(title_text="Time [s]", row=2, col=1)

    fig.update_yaxes(title_text="X [m]", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Vx [m/s]", row=1, col=1, secondary_y=True)

    fig.update_yaxes(title_text="Y [m]", row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Vy [m/s]", row=2, col=1, secondary_y=True)

    fig.update_layout(
        title="Balloon Horizontal Position and Velocity History",
        legend=dict(x=0.01, y=0.99),
        height=800,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_xyz_position_trajectory_html(
    position_x: np.ndarray,
    position_y: np.ndarray,
    position_z: np.ndarray,
    output_path: Path,
) -> None:
    """X-Y-Z 三次元位置軌跡をプロットしてHTMLファイルに保存する。"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=position_x,
            y=position_y,
            z=position_z,
            mode="lines",
            name="X-Y-Z Position Trajectory",
            hovertemplate=(
                "X: %{x:.1f} m<br>"
                "Y: %{y:.1f} m<br>"
                "Z: %{z:.1f} m"
            ),
        )
    )

    fig.update_layout(
        title="Balloon X-Y-Z Position Trajectory",
        scene=dict(
            xaxis_title="X [m]",
            yaxis_title="Y [m]",
            zaxis_title="Z / Altitude [m]",
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_xyz_position_trajectory_png(
    position_x: np.ndarray,
    position_y: np.ndarray,
    position_z: np.ndarray,
    output_path: Path,
) -> None:
    """X-Y-Z 三次元位置軌跡をプロットしてPNGファイルに保存する。"""
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(
        position_x,
        position_y,
        position_z,
        label="X-Y-Z Position Trajectory",
    )

    ax.scatter(
        position_x[0],
        position_y[0],
        position_z[0],
        marker="o",
        s=40,
        label="Start",
    )

    ax.scatter(
        position_x[-1],
        position_y[-1],
        position_z[-1],
        marker="x",
        s=60,
        label="End",
    )

    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("Z / Altitude [m]")
    ax.set_title("Balloon X-Y-Z Position Trajectory")
    ax.legend()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)