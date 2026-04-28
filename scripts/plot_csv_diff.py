from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    csv_29_path = Path("29.csv")
    csv_28_path = Path("28.csv")

    output_dir = Path("diff_png")
    output_dir.mkdir(parents=True, exist_ok=True)

    df_29 = pd.read_csv(csv_29_path)
    df_28 = pd.read_csv(csv_28_path)

    time_column = "absolute_time"

    if time_column not in df_29.columns:
        raise ValueError(f"{csv_29_path} に {time_column} 列がありません")

    if time_column not in df_28.columns:
        raise ValueError(f"{csv_28_path} に {time_column} 列がありません")

    # ISO8601形式として読む。
    # 小数秒あり/なしが混在していても読めるようにする。
    df_29[time_column] = pd.to_datetime(
        df_29[time_column],
        format="ISO8601",
        utc=True,
    )

    df_28[time_column] = pd.to_datetime(
        df_28[time_column],
        format="ISO8601",
        utc=True,
    )

    merged = pd.merge(
        df_29,
        df_28,
        on=time_column,
        suffixes=("_29", "_28"),
        how="inner",
    )

    if merged.empty:
        raise ValueError("29.csv と 28.csv で一致する absolute_time がありません")

    common_columns = [
        col for col in df_29.columns if col != time_column and col in df_28.columns
    ]

    if not common_columns:
        raise ValueError("比較可能な共通フィールドがありません")

    for field in common_columns:
        col_29 = f"{field}_29"
        col_28 = f"{field}_28"

        values_29 = pd.to_numeric(merged[col_29], errors="coerce")
        values_28 = pd.to_numeric(merged[col_28], errors="coerce")

        diff = values_29 - values_28

        if diff.isna().all():
            print(f"skip non-numeric field: {field}")
            continue

        plt.figure(figsize=(10, 6))
        plt.plot(merged[time_column], diff)
        plt.xlabel("absolute_time")
        plt.ylabel(f"{field} difference")
        plt.title(f"{field}: 29.csv - 28.csv")
        plt.grid(True)
        plt.tight_layout()

        output_path = output_dir / f"{field}.png"
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
