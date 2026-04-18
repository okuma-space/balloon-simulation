from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from environment.atmosphere.layered_temperature_model import calculate_temperature


OUTPUT_DIR = Path("docs")


def run_temperature_simulation() -> tuple[np.ndarray, np.ndarray]:
    """分層大気モデルによる温度を計算するシミュレーションを実行し、高度と温度の配列を返す。"""
    # 50[km]まで100[m]ずつ計算する
    altitudes = np.linspace(0, 50000, 501)
    temperatures = np.array([calculate_temperature(h) for h in altitudes])
    return altitudes, temperatures


def save_temperature_html(
    altitudes: np.ndarray, temperatures: np.ndarray, output_path: Path
) -> None:
    """高度と温度の配列をプロットしてHTMLファイルに保存する。"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=temperatures, y=altitudes, mode="lines", name="Layered Model")
    )
    fig.update_layout(
        title="Layered Atmosphere Model",
        xaxis_title="Temperature [K]",
        yaxis_title="Altitude [m]",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_temperature_png(
    altitudes: np.ndarray, temperatures: np.ndarray, output_path: Path
) -> None:
    """高度と温度の配列をプロットしてPNGファイルに保存する。"""
    plt.figure()
    plt.plot(temperatures, altitudes)
    plt.title("Layered Atmosphere Model")
    plt.xlabel("Temperature [K]")
    plt.ylabel("Altitude [m]")
    plt.grid(True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # シミュレーション実行
    altitudes, temperatures = run_temperature_simulation()

    html_path = OUTPUT_DIR / "html/layered_temperature.html"
    png_path = OUTPUT_DIR / "png/layered_temperature.png"

    # htmlとpngを保存
    save_temperature_html(altitudes, temperatures, html_path)
    save_temperature_png(altitudes, temperatures, png_path)

    print(f"saved: {html_path}")
    print(f"saved: {png_path}")


if __name__ == "__main__":
    main()
