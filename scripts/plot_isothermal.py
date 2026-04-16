import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# py/ を import path に追加
sys.path.append("./py")

from environment.atmosphere.isothermal_model import calculate_density


OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # 高度 [m]
    altitudes = np.linspace(0, 40000, 500)

    # 密度計算
    densities = [calculate_density(h) for h in altitudes]

    # プロット
    plt.figure()
    plt.plot(densities, altitudes)

    plt.xlabel("Air Density [kg/m^3]")
    plt.ylabel("Altitude [m]")
    plt.title("Isothermal Atmosphere Model")
    plt.grid()

    # 保存
    output_path = OUTPUT_DIR / "isothermal_density.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close()

    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()