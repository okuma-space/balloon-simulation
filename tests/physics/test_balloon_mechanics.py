import pytest
from physics import balloon_mechanics

# 許容誤差1[%]
REL_TOL = 0.01


def test_calculate_ground_volume():

    # 100000[m^3], 35[km]のときの地表面上での体積を計算
    ground_volume = balloon_mechanics.calculate_ground_volume(35000.0, 100000.0)
    assert ground_volume == pytest.approx(1577, rel=REL_TOL)

    # 逆算して一致することを確認
    volume_at_altitude = balloon_mechanics.calculate_volume_at_altitude(
        35000.0, ground_volume
    )
    assert volume_at_altitude == pytest.approx(100000.0, rel=REL_TOL)
