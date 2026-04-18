import pytest
from environment.atmosphere import layered_temperature_model

# 許容誤差2.5[%]
REL_TOL = 0.025

# テスト用検証データとして1976 Standard Atmosphere Tableを採用する
# https://www.pdas.com/atmosTable1SI.html
test_data = [
    (0, 288.1),
    (2000, 275.2),
    (4000, 262.2),
    (6000, 249.2),
    (8000, 236.2),
    (10000, 223.3),
    (12000, 216.6),
    (14000, 216.6),
    (16000, 216.6),
    (18000, 216.6),
    (20000, 216.6),
    (22000, 218.6),
    (24000, 220.6),
    (26000, 222.5),
    (28000, 224.5),
    (30000, 226.5),
    (32000, 228.5),
    (34000, 233.7),
    (36000, 239.3),
    (38000, 244.8),
    (40000, 250.4),
    (42000, 255.9),
    (44000, 261.4),
    (46000, 266.9),
    (48000, 270.6),
    (50000, 270.6),
]


@pytest.mark.parametrize("altitude, ref_temperature", test_data)
def test_layered_temperature_model(altitude, ref_temperature):
    """
    1976 US Standard Atmosphere Tableに対して誤差10[%]以内であることを検証テストする
    """
    model_temperature = layered_temperature_model.calculate_temperature(altitude)

    rel_error = abs(model_temperature - ref_temperature) / ref_temperature

    assert rel_error <= REL_TOL
