import pytest
from environment.atmosphere import isothermal_model

# 許容誤差10[%]
REL_TOL = 0.1

# テスト用検証データとして1976 Standard Atmosphere Tableを採用する
# https://atmos.nmsu.edu/planetary_datasets/earth_temppres.html
test_data = [
    (0, 1.225),
    (1000, 1.1116),
    (2000, 1.0065),
    (3000, 0.9091),
    (4000, 0.8191),
    (5000, 0.7361),
    (6000, 0.6597),
    (7000, 0.5895),
    (8000, 0.5252),
    (9000, 0.4663),
    (10000, 0.4127),
    (11000, 0.3639),
    (12000, 0.3108),
    (13000, 0.2655),
    (14000, 0.2268),
    (15000, 0.1937),
]


@pytest.mark.parametrize("altitude, ref_density", test_data)
def test_isothermal_density_accuracy(altitude, ref_density):
    """
    1976 US Standard Atmosphere Tableに対して誤差10[%]以内であることを検証テストする
    """
    model_density = isothermal_model.calculate_density(altitude)

    rel_error = abs(model_density - ref_density) / ref_density

    assert rel_error <= REL_TOL
