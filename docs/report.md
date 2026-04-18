
# シミュレーション結果サマリ
## 1.気球上昇運動シミュレーション



## 2.Isothermal Atomosphere model(等温大気モデル)
isothermal_model.pyにて計算。
1976 US Standard Atmosphere Tableに対して誤差10[%]以内であることを検証テストしている。
### 静的表示
![density](https://okuma-space.github.io/balloon-simulation/png/isothermal_density.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/isothermal_density.html)



## 3.気球上昇運動シミュレーション過去version
### version0.1
version0.1として気球を球体近似した抗力を追加(https://github.com/okuma-space/balloon-simulation/pull/9)

一定高度で定常浮遊状態には入れる事が確認できた
- 気体密度 0.178[kg/m^3] (ヘリウム) (https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0[m^3]
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.1.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.1.html)


### version0.0
初期versionとして気球内部の気体密度と外部の大気密度差から発生する浮力のみ考慮(https://github.com/okuma-space/balloon-simulation/pull/8)

抗力が発生しないので速度の減衰が発生せずに振動をしている。
- 気体密度 0.178[kg/m^3] (ヘリウム) (https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0[m^3]
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.0.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.0.html)