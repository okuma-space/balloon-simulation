import environment.atmosphere.isothermal_model as isothermal_model

def test_calculate_density():
    # 海面高度での大気密度はAIR_DENSITY_SEA_LEVELと等しいことを確認
    assert isothermal_model.calculate_density(0) == isothermal_model.AIR_DENSITY_SEA_LEVEL

    # 高度1000mでの大気密度がAIR_DENSITY_SEA_LEVELより小さいことを確認
    assert isothermal_model.calculate_density(1000) < isothermal_model.AIR_DENSITY_SEA_LEVEL

    # 高度5000mでの大気密度がAIR_DENSITY_SEA_LEVELより小さいことを確認
    assert isothermal_model.calculate_density(5000) < isothermal_model.AIR_DENSITY_SEA_LEVEL