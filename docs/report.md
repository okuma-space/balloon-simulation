
# シミュレーション自習結果サマリ
## 1.気球上昇運動シミュレーション
TODO ここに最終レポートを書く
主要な処理も書く


## 2 ダイナミクスモデル
現在は鉛直方向のみの1自由度ダイナミクスを対象とし，以下の力学モデルを考慮している．

また時間積分には4次のRunge-Kutta法を用いている．

### 2.1 浮力モデル
浮力は以下で与えられる：

F_b = (ρ_ext - ρ_int) V g

ここで，ρ_ext は外部大気密度 [kg/m^3]，ρ_int は気球内部のガス密度 [kg/m^3]，
V は気球体積 [m^3]，g は重力加速度 [m/s^2] である．

（気球工学 P.15 (2.4)）

### 2.2 抗力モデル
抗力は速度方向を考慮し，以下でモデル化する：

F_d = (1/2) ρ C_d A |v_rel| v_rel

ここで，ρ は外部流体密度 [kg/m^3]，C_d は抗力係数，A は投影面積 [m^2]，
v_rel は流体に対する相対速度ベクトル [m/s] である．

本モデルでは抗力の向きを表現するため，速度ベクトルの符号を保持した形で実装している．

（気球工学 P.53 (2.62)）

### 2.3 合力モデルと鉛直方向加速度
鉛直方向の合力 F_net は

F_net = F_b + F_d - m g

とし，ここで m は気球の総質量（ペイロード＋ガス）である．

加速度は以下で計算する：

a = F_net / m

## 3 気球モデル
気球の状態量として以下を考慮している.
- 時刻 [UTC]
- 位置 [m]
- 速度 [m/s]
- 体積 [m^3]
- ガス温度 [K]
- ガス質量 [kg]
- ペイロード質量 [kg]

### 3.1 体積モデル
体積は高度の関数として一意に決まると仮定し理想気体かつ温度一定の近似のもとで，以下の関係を用いる

V(h) = V_0 * ρ_0 / ρ(h)

ここでV_0 は地表面における体積 [m^3]，ρ_0 は地表面の大気密度, ρ(h) は高度 h における大気密度である．

### 3.2 温度モデル
TBD


## 4 Environment models(環境モデル)
現在のシミュレーションで採用している環境モデルについて示す.

### 4.1 Isothermal Atmosphere model(等温大気モデル)
大気密度の計算は等温大気モデルを採用しenvironment/atomosphere/isothermal_model.pyにて計算している.

1976 US Standard Atmosphere Table と比較し,誤差10 [%]以内であることを確認している.

#### Figures
等温大気モデルにおける高度と密度の関係を以下示す.

![density](https://okuma-space.github.io/balloon-simulation/png/isothermal_density.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/isothermal_density.html)

### 4.2 Layered Temperature Model(分層大気温度モデル)
大気温度の計算は1976 US Standard Atmosphere Tableをベースに以下のように分層化した.

- 1層(0~12[km])
  - 288.1[K]から216.6[K]までの線形補間
- 2層(12~20[km])
  - 216.6[K]一定
- 3層(20~35[km])
  - 216.6[K]から235[K]までの線形補間
- 4層(35~50[km])
  - 235[K]から270[K]までの線形補間
- 5層 (>50 km)
  - 270[K]一定(将来的にはここも線形補間とする) [issues](https://github.com/okuma-space/balloon-simulation/issues/18)


数値計算はenvironment/atomosphere/layered_temperature_model.pyにて計算している.

1976 US Standard Atmosphere Table と比較し,誤差 [2.5%]以内であることを確認している.

#### Figures
分層大気温度モデルにおける高度と温度の関係を以下示す.

![temperature](https://okuma-space.github.io/balloon-simulation/png/layered_temperature.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/layered_temperature.html)

## 5 プログラム実装
### 5.1 実行手順
README/mnにて記載.






## Appendix.過去versionの検証ログ(保存/振り返り用)
### version0.4
version0.4として数値積分の方法をオイラー法から4次のRunge-Kutta方へと変更した.

計算モデルはver0.3と共通で,計算ステップを1[sec]とした時には結果に大きな差は見られなかった.

計算ステップを1.5[sec]とする以下のグラフのようになる.

1枚目にオイラー法，2枚目にRunge-Kutta法の結果を示す．

オイラー法では初期近辺で数値的な振動（擾乱）が発生しており,Runge-Kutta法ではそれが抑制される改善が見えた.

今後よりモデルを高度化していくため,数値安定性および精度の観点から今後はRunge-Kutta法を採用していく.

なお計算ステップを2.0[sec]とするとオイラー法は数値発散（オーバーフロー）により計算が破綻するが,Runge-Kutta法は初期近辺で数値的な振動（擾乱）が発生しつつも計算可能であった.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.4)

[PR](https://github.com/okuma-space/balloon-simulation/pull/22)

#### Figures
![pos_vel](https://okuma-space.github.io/balloon-simulation/png/balloon_posvel_trajectory_0.4.png)
![pos_vel_rk](https://okuma-space.github.io/balloon-simulation/png/balloon_posvel_trajectory_0.4_rk.png)



___
___

### version0.3
version0.3として気球の体積変化を追加しシミュレートした.
パラメタとして地表面での体積,ガス質量を基に外気圧とガス圧から体積を変動させた.
計算収束のために,体積には上限値を設定している.

実験はver0.2同様に気球工学P.16に従って,以下の条件で実験をした.
- 地表体積 1578.0 [m^3]
- ガス質量 230.0 [kg]
- ペイロード質量 500.0 [kg]

文献ではこの条件で高度35 [km]まで上昇可能と記載されており,実験では42 [km]程度まで上昇した.

文献においては35 [km]にて体積は100000 m^3とあったため,等温大気モデルを用いて地表での体積を逆算し1578 m^3とした.

この対応によってver0.2で存在した初速が40 [m/s](144 [km/h])から15 [m/s](54 [km/h])へと減速に成功した.

体積上限を設定しなかった場合は気球が上昇をし続けるという問題があったが,体積上限の設定によって適切に定常浮遊へと移行するようになった.

グラフには考察のため体積,断面積,ガス密度の推移も追加した.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.3)

[PR](https://github.com/okuma-space/balloon-simulation/pull/12)

#### Figures
![pos_vel](https://okuma-space.github.io/balloon-simulation/png/balloon_posvel_trajectory_0.3.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/png/balloon_volume_area_trajectory_0.3.png)
![gas_density](https://okuma-space.github.io/balloon-simulation/png/balloon_gas_density_trajectory_0.3.png)

#### Interactive Figures
[pos_vel](https://okuma-space.github.io/balloon-simulation/html/balloon_posvel_trajectory_0.3.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/balloon_volume_area_trajectory_0.3.html)

[gas_density](https://okuma-space.github.io/balloon-simulation/html/balloon_gas_density_trajectory_0.3.html)

___
___

### version0.2
version0.2として気球の質量をガス質量とペイロード質量に分離した

気球工学P.16に従って,以下の条件で実験をした
- 気体密度 0.0023 [kg/m^3]
- 体積 100000.0 [m^3]
- ガス質量 230.0 [kg]
- ペイロード質量 500.0 [kg]

文献ではこの条件で高度35 [km]まで上昇可能と記載されており,実験では42 [km]程度まで上昇した.
高精度ではないが簡易モデルとしてはオーダーはそこまで大きく外れていない.
一方で初速が40 [m/s](144 [km/h])と非常に高速であり,これは気球体積を一定値としているため地表付近での浮力が高くなりすぎている可能性がある.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.2)

[PR](https://github.com/okuma-space/balloon-simulation/pull/10)

#### Figures
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.2.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.2.html)

___
___

### version0.1
version0.1として気球を球体近似した抗力を追加

一定高度で定常浮遊状態には入れる事が確認できた
- 気体密度 0.178 [kg/m^3] (ヘリウム) [ref](https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0 [m^3]

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.1)

[PR](https://github.com/okuma-space/balloon-simulation/pull/9)

#### Figures
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.1.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.1.html)

___
___

### version0.0
初期versionとして気球内部の気体密度と外部の大気密度差から発生する浮力のみ考慮

抗力が発生しないので速度の減衰が発生せずに振動をしている.
- 気体密度 0.178 [kg/m^3] (ヘリウム) [ref](https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
- 体積 1.0 [m^3]

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.0)

[PR](https://github.com/okuma-space/balloon-simulation/pull/8)

#### Figures
![trajectry](https://okuma-space.github.io/balloon-simulation/png/balloon_trajectory_0.0.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/balloon_trajectory_0.0.html)