
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
### version0.3
version0.3として気球の体積変化をシミュレートした
パラメタとして地表面での体積、ガス質量を基に外気圧とガス圧から体積を変動させた
計算収束のために、体積には上限値を設定している

実験はver0.2同様に気球工学P.16に従って、以下の条件で実験をした
- 地表体積 1578.0[m^3]
- ガス質量 230.0[kg]
- ペイロード質量 500.0[kg]

文献ではこの条件で高度35[km]まで上昇可能と記載されており、実験では42[km]程度まで上昇した.

文献においては35[km]にて体積は100000[m^3]とあったため、等温大気モデルを用いて地表での体積を逆算し1578[m^3]とした.

この対応によってver0.2で存在した初速が40[m/s](144[km/h])から15[m/s](54[km/h])へと減速に成功した.

体積上限を設定しなかった場合は気球が上昇をし続けるという問題があったが、体積上限の設定によって適切に定常浮遊へと移行するようになった.

グラフには考察のため体積,断面積,ガス密度の推移も追加した.

[PR](https://github.com/okuma-space/balloon-simulation/pull/12)

### Figures
![pos_vel](https://okuma-space.github.io/balloon-simulation/png/balloon_posvel_trajectory_0.3.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/png/balloon_volume_area_trajectory_0.3.png)
![gas_density](https://okuma-space.github.io/balloon-simulation/png/balloon_gas_density_trajectory_0.3.png)

### Interactive Figures
[pos_vel](https://okuma-space.github.io/balloon-simulation/html/balloon_posvel_trajectory_0.3.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/balloon_volume_area_trajectory_0.3.html)

[gas_density](https://okuma-space.github.io/balloon-simulation/html/balloon_gas_density_trajectory_0.3.html)

### version0.2
version0.2として気球の質量をガス質量とペイロード質量に分離した

気球工学P.16に従って、以下の条件で実験をした
- 気体密度 0.0023[kg/m^3]
- 体積 100000.0[m^3]
- ガス質量 230.0[kg]
- ペイロード質量 500.0[kg]

文献ではこの条件で高度35[km]まで上昇可能と記載されており、実験では42[km]程度まで上昇した。
高精度ではないが簡易モデルとしてはオーダーはそこまで大きく外れていない。
一方で初速が40[m/s](144[km/h])と非常に高速であり、これは気球体積を一定値としているため地表付近での浮力が高くなりすぎている可能性がある。

[PR](https://github.com/okuma-space/balloon-simulation/pull/9)
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.2.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.2.html)



### version0.1
version0.1として気球を球体近似した抗力を追加

一定高度で定常浮遊状態には入れる事が確認できた
- 気体密度 0.178[kg/m^3] (ヘリウム) [ref](https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0[m^3]

[PR](https://github.com/okuma-space/balloon-simulation/pull/9)
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.1.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.1.html)


### version0.0
初期versionとして気球内部の気体密度と外部の大気密度差から発生する浮力のみ考慮

抗力が発生しないので速度の減衰が発生せずに振動をしている。
- 気体密度 0.178[kg/m^3] (ヘリウム)[ref] (https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0[m^3]

[PR](https://github.com/okuma-space/balloon-simulation/pull/8)
### 静的表示
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.0.png)

### インタラクティブ表示
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.0.html)