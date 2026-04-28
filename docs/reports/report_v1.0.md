
# シミュレーション自習結果サマリ
## 1.気球上昇下降運動シミュレーション
pythonにて簡易的な気球の上昇下降シミュレーションを実装した.

気球のパラメタ及び計算条件はconfig.jsonにて定義しており,シミュレーション実行結果となる高度/速度グラフは以下となる.

横軸は離陸からの秒数を示している.

![pos_vel](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.6.png)

Interactive Figures

[pos_vel](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_posvel_trajectory_0.5.html)

運用シナリオとしては,離陸して最高地点到達後に10分毎に断続的にガスを放出する想定で以下の制御スケジュールを想定した.

```bash
- 2026-01-01T00:00:00Z 離陸
- 2026-01-01T01:40:00Z ガスの放出開始
  - 2026-01-01T01:50:00Z ガスの放出終了
- 2026-01-01T02:00:00Z ガスの放出開始
  - 2026-01-01T02:10:00Z ガスの放出終了
- 2026-01-01T02:20:00Z ガスの放出開始
  - 2026-01-01T02:30:00Z ガスの放出終了
- 2026-01-01T02:40:00Z ガスの放出開始
  - 2026-01-01T02:50:00Z ガスの放出終了
- 2026-01-01T03:00:00Z ガスの放出開始
  - 2026-01-01T03:10:00Z ガスの放出終了
- 2026-01-01T03:20:00Z ガスの放出開始
  - 2026-01-01T03:28:00Z ガスの放出終了
```

最後の放出は着陸速度を緩めるために8分間だけを想定した.

シミュレーション結果より，気球は約2500 [sec]程で最高高度として約42 [km]近辺に到達した.その後しばらく定常浮遊し約11500 [sec]から下降を開始して，約15500 [sec]で地上へ到達した.
鉛直速度も最高到達点付近で約 0 [m/s]近傍に収束しその後は約11500 [sec] から負側へ転じ，着地時に再び0 [m/s]に収束した。

以下はガスの密度と質量のグラフとなる.

![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_gas_state_history_0.6.png)

Interactive Figures

[gas_state](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_gas_state_history_0.5.html)

序盤の上昇フェーズで約2500 [sec]までガス密度が低下し,下降フェーズで約12500 [sec]から再び上昇していることが確認できる.

ガスの質量についても初期値として230 [kg]であったものが約6000 [sec]辺りから放出が始まり,段階的に約90 [kg]近傍まで下降していることが確認できる.

以下は気球の体積と表面積についてのグラフである.

![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_volume_area_history_0.6.png)

Interactive Figures

[volume_area](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_volume_area_history_0.6.html)

後述するように気球には最大体積を設定しているため,高度が上昇するにつれ約2500 [sec]までは膨張しつつもその後一定値でとどまっていることが確認できる.

その後ガスの放出が始まり約11500 [sec]近傍から減少を開始している.

以下は気球のガス温度のグラフとなる.

![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_temperature_history_0.6.png)

Interactive Figures

[temperature](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_temperature_history_0.5.html)

なめらかではあるが5.2で後述する分層大気モデルを時間遅れで追従していることが確認できる.

まとめ
- 上昇、定常浮遊、下降の3フェーズを再現できた
- 段階的ベントにより穏やかな降下が得られ,着陸直前速度は約6 [m/s]であった


## 2 ダイナミクスモデル
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

a = F_net / m

## 3 気球モデル
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
### 3.1 体積/面積モデル
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

### 3.2 熱モデル
大気温度は 5.2 の分層大気温度モデルを用いており,内部温度は以下の簡易モデルで更新している.
```bash
T_in,new = T_in,old + (T_out - T_in,old) / 1000
```
ここでT_in,old は更新前の内部温度,T_in,new は更新後の内部温度,T_out は外部温度を示す.

本モデルでは,内部温度が外部温度に対して緩やかに追従する一次遅れ近似として扱っている.

熱遅れの詳細,日射,放射冷却などは考慮していない.

### 3.3 内部圧力モデル
内部圧力は理想気体の状態方程式を用いて以下で計算をしている.
```bash
P = mRsT / V
```
ここで P は内部圧力 [Pa], m はガス質量 [kg], Rs は比気体定数 [J/(kg·K)], T は温度 [K] であり, V は体積モデルで計算された値を用いる.

現在は内部圧力は体積計算には用いておらず,4.1の下降制御時の内外圧力差計算にのみ用いている.

## 4 制御モデル
### 4.1 下降制御
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







## 5 Environment models(環境モデル)
現在のシミュレーションで採用している環境モデルについて示す.

### 5.1 Isothermal Atmosphere model(等温大気モデル)
大気密度の計算は等温大気モデルを採用しenvironment/atomosphere/isothermal_model.pyにて計算している.

1976 US Standard Atmosphere Table と密度値を比較し，相対誤差が概ね10 [%]以内であることを確認している。

#### Figures
等温大気モデルにおける高度と密度の関係を以下示す.

![density](https://okuma-space.github.io/balloon-simulation/images/generated/isothermal_density.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/isothermal_density.html)

### 5.2 Layered Temperature Model(分層大気温度モデル)
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
### version0.6
version0.6として温度モデルを改善した.

挙動に大きな違いはないが,温度グラフがより緩やかに分層大気モデルを追従するようになったことが確認できる.

また温度変化が緩やかになったため,気球モデルの数値次第で着陸後にある程度時間が経つとガスが温まり再浮遊するケースも散見された.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.6)

[PR](https://github.com/okuma-space/balloon-simulation/pull/27)

#### Figures
![pos_vel](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.6.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_volume_area_history_0.6.png)
![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_gas_state_history_0.6.png)
![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_temperature_history_0.6.png)

#### Interactive Figures
[pos_vel](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_posvel_trajectory_0.6.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_volume_area_trajectory_0.6.html)

[gas_state](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_gas_state_history_0.6.html)

[temperature](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_temperature_history_0.6.html)

___
___


### version0.5
version0.5としてガスの放出による下降制御を導入した.

導入にあたって熱モデルが必要だったので簡易的に外気温と同一と見なした.

同様に体積モデルを熱を考慮した理想気体の状態方程式に基づくモデルに変更した.

下降制御は完全放出すると垂直落下したため,まずは開始終了時刻の配列を与えるスケジュール式として,地表面に帰還するシナリオを組んだ.

想定通りに緩やかな帰還が実現できている.

また温度,体積,なども上昇フェーズと下降フェーズで想定通りの挙動を示している.

[Repository](https://github.com/okuma-space/balloon-simulation/tree/v0.5)

[PR](https://github.com/okuma-space/balloon-simulation/pull/26)

#### Figures
![pos_vel](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.5.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_volume_area_history_0.5.png)
![gas_state](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_gas_state_history_0.5.png)
![temperature](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_temperature_history_0.5.png)

#### Interactive Figures
[pos_vel](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_posvel_trajectory_0.5.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_volume_area_trajectory_0.5.html)

[gas_state](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_gas_state_history_0.5.html)

[temperature](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_temperature_history_0.5.html)

___
___


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
![pos_vel](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.4.png)
![pos_vel_rk](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.4_rk.png)

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
![pos_vel](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_posvel_trajectory_0.3.png)
![volume_area](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_volume_area_trajectory_0.3.png)
![gas_density](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_gas_density_trajectory_0.3.png)

#### Interactive Figures
[pos_vel](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_posvel_trajectory_0.3.html)

[volume_area](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_volume_area_trajectory_0.3.html)

[gas_density](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_gas_density_trajectory_0.3.html)

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
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_trajectory_0.2.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_trajectory_0.2.html)

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
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_trajectory_0.1.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_trajectory_0.1.html)

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
![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/v0/balloon_trajectory_0.0.png)

#### Interactive Figures
[graph](https://okuma-space.github.io/balloon-simulation/html/v0/balloon_trajectory_0.0.html)