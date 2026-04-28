
# シミュレーション自習結果サマリ
## 1.気球水平運動シミュレーション
pythonにて簡易的な気球の水平シミュレーションを実装した.

TBD

まとめ


## 2 上下運動ダイナミクスモデル
現在は鉛直方向のみの1自由度ダイナミクスを対象とし，以下の力学モデルを考慮している．

また時間積分には4次のRunge-Kutta法を用いている．

### 2.1 浮力モデル
浮力は以下で与えられる：
```bash
F_b = (ρ_ext - ρ_int) V g
```
ここで，ρ_ext は外部大気密度 [kg/m^3]，ρ_int は気球内部のガス密度 [kg/m^3]，
V は気球体積 [m^3]，g は重力加速度 [m/s^2] である．

（気球工学 P.15 (2.4)）

### 2.2 抗力モデル
抗力は速度方向を考慮し，以下でモデル化する：
```bash
F_d = (1/2) ρ C_d A |v_rel| v_rel
```
ここで，ρ は外部流体密度 [kg/m^3]，C_d は抗力係数，A は投影面積 [m^2]，
v_rel は流体に対する相対速度ベクトル [m/s] である．

本モデルでは抗力の向きを表現するため，速度ベクトルの符号を保持した形で実装している．

（気球工学 P.53 (2.62)）

なお抗力計算には3.1で示しす体積/断面積モデルを用いる.

### 2.3 合力モデルと鉛直方向加速度
鉛直方向の合力 F_net は
```bash
F_net = F_b + F_d - m g
```
とし，ここで m は気球の総質量であり,現在は膜を考慮しない（ペイロード＋ガス）である．

加速度は以下で計算する：
```bash
a = F_net / m
```

## 3 水平運動ダイナミクスモデル
TBD



## 4 気球モデル
気球の状態量として以下を考慮している.
```bash
- 時刻 [UTC]
- 位置 [m]
- 速度 [m/s]
- 気球体積 [m^3]
- 気球最大体積 [m^3]
- ガス温度 [K]
- ガス質量 [kg]
- 揚力ガスの種類 (ヘリウム or 水素)
- ペイロード質量 [kg]
- ペイロード断面積 [m^2]
- ペイロード抗力係数 Cd [-]（ペイロードは立方体近似として約 1.1）
- 気球抗力係数 Cd [-]（気球は球体近似として約 0.47）
- 排気弁の総開口部面積 [m^2]
- 排気弁の流量係数 約 0.61
```

### 4.1 体積/面積モデル
気球の形状は常に真球と仮定しており,体積は理想気体の状態方程式より以下の簡易モデルで計算をしている.
```bash
PV = mR_sT

V = mR_sT/P
```
ここで P は外部圧力 [Pa], m はガス質量 [kg], R_s は比気体定数 [J/(kg·K)], T は温度 [K]である.

外部圧力は5.1の等温大気モデルを用いて算出しており,体積の計算では内部圧力=外部圧力と近似して計算している.

なお気球には最大体積を設定しており,ある一定以上の体積にはならないように計算している.これは気球が破裂して際限なく体積が上昇するのではなく,膜によって留められていることをシミュレートしている.

抗力計算に用いる断面積は球体の断面積として以下の計算で半径rを算出している.
```bash
V = (4/3) * π * r^3  =>  r = (3V / (4π))^(1/3)
```
ここで算出された半径で円近似として以下で断面積を計算している.
```bash
A=πr^2
```
なおペイロードも断面積を保持しており,現在は簡易モデルとして有効断面積を max(気球断面積, ペイロード断面積) で近似して抗力計算に用いている.

### 4.2 熱モデル
大気温度は 5.2 の分層大気温度モデルを用いており,内部温度は以下の簡易モデルで更新している.
```bash
T_in,new = T_in,old + (T_out - T_in,old) / 2000
```
ここでT_in,old は更新前の内部温度,T_in,new は更新後の内部温度,T_out は外部温度を示す.

本モデルでは,内部温度が外部温度に対して緩やかに追従する一次遅れ近似として扱っている.

熱遅れの詳細,日射,放射冷却などは考慮していない.

### 4.3 内部圧力モデル
内部圧力は理想気体の状態方程式を用いて以下で計算をしている.
```bash
P = mRsT / V
```
ここで P は内部圧力 [Pa], m はガス質量 [kg], Rs は比気体定数 [J/(kg·K)], T は温度 [K] であり, V は体積モデルで計算された値を用いる.

現在は内部圧力は体積計算には用いておらず,4.1の下降制御時の内外圧力差計算にのみ用いている.

## 5 制御モデル
### 5.1 下降制御
現在簡易的に排気弁からのガス排出による下降制御をシミュレートしている．

排気による浮揚ガスの体積流量 Q [m³/s] は以下で近似する（ref. 気球工学 P56 式 (2.79)）
```bash
Q = Cd · A · √(2 ΔP / ρ)
```
ここで，
```bash
- Cd : 流量係数 [-]  
- A  : 排気弁開口面積 [m²]  
- ρ  : 内部ガス密度 [kg/m³]  
- ΔP : 排気弁開口部における内外圧力差 [Pa]  
```
また，質量流量 ṁ [kg/s] は以下で求める：
```bash
ṁ = ρ Q
```
なお流量係数 Cd は鋭いエッジを持つオリフィス流れの代表値として 0.61 を使用する．  
https://wiki.sustainabletechnologies.ca/wiki/Flow_through_an_orifice

現在排気はスケジュール式により制御しており，configファイルにて排気イベント（開始時刻・終了時刻の組）のリストを定義している．

## 6 Environment models(環境モデル)
現在のシミュレーションで採用している環境モデルについて示す.

### 6.1 Isothermal Atmosphere model(等温大気モデル)
大気密度の計算は等温大気モデルを採用しenvironment/atomosphere/isothermal_model.pyにて計算している.

1976 US Standard Atmosphere Table と密度値を比較し，相対誤差が概ね10 [%]以内であることを確認している。

#### Figures
等温大気モデルにおける高度と密度の関係を以下示す.

![density](https://okuma-space.github.io/balloon-simulation/images/generated/isothermal_density.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/isothermal_density.html)

### 6.2 Layered Temperature Model(分層大気温度モデル)
大気温度の計算は1976 US Standard Atmosphere Tableをベースに以下のように分層化した.
```bash
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
```

数値計算はenvironment/atomosphere/layered_temperature_model.pyにて計算している.

1976 US Standard Atmosphere Table と温度値を比較し，相対誤差が概ね2.5 [%]以内であることを確認している.

https://www.pdas.com/atmosTable1SI.html

#### Figures
分層大気温度モデルにおける高度と温度の関係を以下示す.

![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/layered_temperature.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/layered_temperature.html)


## Appendix. 過去versionの検証ログ(保存/振り返り用)
### version1.1
version1.1としてpropagatorを統合

気球のstatusに関わる変数(体積/温度など)と位置速度をまとめて状態ベクトルとして統合.

状態ベクトルを全てルンゲクッタ法で積分するように改修した.

改修後の伝搬結果も特に問題なく出力されていることを確認した.

気球のサイズをsmall(ペイロード質量 3 [kg]) middle (ペイロード質量 500 [kg]) middle (ペイロード質量 500 [kg]) large (ペイロード質量 1100 [kg])と三種シミュレーション実験した.

いずれも高高度に上昇したのち,ガスの排気スケジュールに従って下降していることが確認できる.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v1.1)

[PR](https://github.com/okuma-space/balloon-simulation/pull/9)


#### small balloon
- payload_mass: 6.0 [kg]
- max_volume: 1000.0 [m^3]
- initial_gas_mass: 1.5 [kg]
- vent_schedule: 
  - ["2026-01-01T01:30:00Z", "2026-01-01T01:32:00Z"]
  
##### Figures small
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_posvel_trajectory_1.1_S.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_volume_area_history_1.1_S.png)
![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_gas_state_histor_1.1_S.png)
![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_temperature_history_1.1_S.png)

##### Interactive Figures small
[trajectry](https://okuma-space.github.io/balloon-simulation/html/balloon_posvel_trajectory_1.1_S.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/balloon_volume_area_history_1.1_S.html)

[gas_state](https://okuma-space.github.io/balloon-simulation/html/balloon_gas_state_histor_1.1_S.html)

[temperature](https://okuma-space.github.io/balloon-simulation/html/balloon_temperature_history_1.1_S.html)

#### middle balloon
- payload_mass: 500.0 [kg]
- max_volume: 100000.0 [m^3]
- initial_gas_mass: 230.0 [kg]
- vent_schedule: 
  - ["2026-01-01T01:40:00Z", "2026-01-01T01:50:00Z"]
  - ["2026-01-01T02:00:00Z", "2026-01-01T02:10:00Z"]
  - ["2026-01-01T02:20:00Z", "2026-01-01T02:30:00Z"]
  - ["2026-01-01T02:40:00Z", "2026-01-01T02:50:00Z"]
  - ["2026-01-01T03:00:00Z", "2026-01-01T03:10:00Z"]
  - ["2026-01-01T03:20:00Z", "2026-01-01T04:30:00Z"]

##### Figures middle
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_posvel_trajectory_1.1_M.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_volume_area_history_1.1_M.png)
![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_gas_state_histor_1.1_M.png)
![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_temperature_history_1.1_M.png)

###### Interactive Figures middle
[trajectry](https://okuma-space.github.io/balloon-simulation/html/balloon_posvel_trajectory_1.1_M.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/balloon_volume_area_history_1.1_M.html)

[gas_state](https://okuma-space.github.io/balloon-simulation/html/balloon_gas_state_histor_1.1_M.html)

[temperature](https://okuma-space.github.io/balloon-simulation/html/balloon_temperature_history_1.1_M.html)

#### large balloon
- payload_mass: 1100.0 [kg]
- max_volume: 500000.0 [m^3]
- initial_gas_mass: 250 [kg]
- vent_schedule: 
  - ["2026-01-01T01:30:00Z", "2026-01-01T01:40:00Z"]
  - ["2026-01-01T01:50:00Z", "2026-01-01T02:00:00Z"]
  - ["2026-01-01T02:10:00Z", "2026-01-01T02:20:00Z"]
  - ["2026-01-01T02:30:00Z", "2026-01-01T02:40:00Z"]
  - ["2026-01-01T02:50:00Z", "2026-01-01T03:00:00Z"]
  - ["2026-01-01T03:10:00Z", "2026-01-01T03:20:00Z"]
  - ["2026-01-01T03:30:00Z", "2026-01-01T03:40:00Z"]
  - ["2026-01-01T03:50:00Z", "2026-01-01T03:57:00Z"]

###### Figures large
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_posvel_trajectory_1.1_L.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_volume_area_history_1.1_L.png)
![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_gas_state_histor_1.1_L.png)
![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/balloon_temperature_history_1.1_L.png)

###### Interactive Figures large
[trajectry](https://okuma-space.github.io/balloon-simulation/html/balloon_posvel_trajectory_1.1_L.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/balloon_volume_area_history_1.1_L.html)

[gas_state](https://okuma-space.github.io/balloon-simulation/html/balloon_gas_state_histor_1.1_L.html)

[temperature](https://okuma-space.github.io/balloon-simulation/html/balloon_temperature_history_1.1_L.html)
