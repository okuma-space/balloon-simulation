
# 簡易レポート
## 気球上昇運動シミュレーション



## Isothermal Atomosphere model(等温大気モデル)
isothermal_model.pyにて計算。
1976 US Standard Atmosphere Tableに対して誤差10[%]以内であることを検証テストしている。
### 静的表示
![density](https://okuma-space.github.io/balloon-simulation/png/isothermal_density.png)

### インタラクティブ
[graph](https://okuma-space.github.io/balloon-simulation/html/isothermal_density.html)



## 気球上昇運動シミュレーション過去version
### version0.0
初期versionとして気球内部の気体密度と外部の大気密度差から発生する浮力のみ考慮。
抗力が発生しないので速度の減衰が発生せずに振動をしている。
- 気体密度 0.178[kg/m^3] (ヘリウム) (https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0[m^3]
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.0.png)

### インタラクティブ
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.0.html)