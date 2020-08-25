import numpy as np
from scipy.special import lambertw

from heat_exchanger import HeatExchanger
from heat_exchanger_reverse import HeatExchangerReverse

inlet_temperatures = [80.0, 20.0]
film_heat_transfer_coefficients = [1, 1]
heat_capacity_flows = [5, 4]
heat_load = 100
mixer_type_hot = 'none'
mixer_type_cold = 'none'
mixer_fraction_hot = 0
mixer_fraction_cold = 0


def setup_heat_exchanger():
    """Setup coefficients of the heat exchanger class"""
    return HeatExchanger(
        inlet_temperatures=inlet_temperatures,
        film_heat_transfer_coefficients=film_heat_transfer_coefficients,
        heat_capacity_flows=heat_capacity_flows,
        heat_load=heat_load,
        mixer_type_hot=mixer_type_hot,
        mixer_type_cold=mixer_type_cold,
        mixer_fraction_hot=mixer_fraction_hot,
        mixer_fraction_cold=mixer_fraction_cold)


def setup_model():
    """Setup coefficients for testing the reversed heat exchanger class"""
    h = setup_heat_exchanger()
    return HeatExchangerReverse(
        inlet_temperatures=inlet_temperatures,
        film_heat_transfer_coefficients=film_heat_transfer_coefficients,
        heat_capacity_flows=heat_capacity_flows,
        heat_load=heat_load,
        existent_area=h.area), h


def test_overall_heat_transfer_coefficient():
    m, h = setup_model()
    assert m.overall_heat_transfer_coefficient == h.overall_heat_transfer_coefficient


def test_outlet_temperatures():
    m, h = setup_model()
    assert m.outlet_temperature_hot_stream == h.outlet_temperature_hot_stream
    assert m.outlet_temperature_cold_stream == h.outlet_temperature_cold_stream


def test_area_no_mixer():
    m, h = setup_model()
    assert m.area_no_mixer == h.area


def test_mixer_type():
    m, _ = setup_model()
    assert m.mixer_type == 'none'
    m.heat_load = 90
    assert m.mixer_type == 'bypass'
    m.heat_load = 110
    assert m.mixer_type == 'admixer'


def test_logarithmic_mean_temperature_difference():
    m, h = setup_model()
    assert m.logarithmic_mean_temperature_difference == h.logarithmic_temperature_difference
    m.heat_load = 90
    logarithmic_mean_temperature_difference = m.heat_load / (h.overall_heat_transfer_coefficient * h.area)
    assert logarithmic_mean_temperature_difference == m.logarithmic_mean_temperature_difference


def test_lambertw():
    # Data from Chen J.J.J.,2019. Logarithmic mean: Chen's approximation or explicit solution?. Computers and Chemical Engineering. 120,1-3.
    inlet_temperatures = [125, 30]
    film_heat_transfer_coefficients = [1, 1]
    heat_capacity_flows = [100, 465.83850931677018633540372670807]
    heat_load = 7500
    existent_area = 500
    m = HeatExchangerReverse(
        inlet_temperatures=inlet_temperatures,
        film_heat_transfer_coefficients=film_heat_transfer_coefficients,
        heat_capacity_flows=heat_capacity_flows,
        heat_load=heat_load,
        existent_area=existent_area)
    m.existent_area = 2 * 175
    m.heat_exchanger_temperature_calculation(mixer_side='cold')
    assert abs(m.heat_exchanger_outlet_temperature_cold_stream - 46.27702305742176) < 10e-1
    dTa = m.heat_exchanger_outlet_temperature_hot_stream - m.heat_exchanger_inlet_temperature_cold_stream
    dTb = m.heat_exchanger_inlet_temperature_hot_stream - m.heat_exchanger_outlet_temperature_cold_stream
    LMTD = (dTa - dTb) / np.log(dTa / dTb)
    UA = heat_load / LMTD
    assert UA == 175


# def test_heat_exchanger_temperatures():
#     m, h = setup_model()
#     m.heat_exchanger_temperature_calculation(mixer_side='none')
#     assert m.heat_exchanger_inlet_temperature_hot_stream == h.heat_exchanger_inlet_temperature_hot_stream
#     assert m.heat_exchanger_outlet_temperature_hot_stream == h.heat_exchanger_outlet_temperature_hot_stream
#     assert m.heat_exchanger_inlet_temperature_cold_stream == h.heat_exchanger_inlet_temperature_cold_stream
#     assert m.heat_exchanger_outlet_temperature_cold_stream == h.heat_exchanger_outlet_temperature_cold_stream
#     m.heat_load = 95  # bypass
#     m.heat_exchanger_temperature_calculation(mixer_side='cold')
#     assert m.heat_exchanger_inlet_temperature_hot_stream == h.heat_exchanger_inlet_temperature_hot_stream
#     assert m.heat_exchanger_outlet_temperature_hot_stream == h.heat_exchanger_inlet_temperature_hot_stream - m.heat_load / m.heat_capacity_flow_hot_stream
#     assert m.heat_exchanger_inlet_temperature_cold_stream == h.heat_exchanger_inlet_temperature_cold_stream

#     dTa = m.heat_exchanger_outlet_temperature_hot_stream - m.heat_exchanger_inlet_temperature_cold_stream
#     dTb = m.heat_exchanger_inlet_temperature_hot_stream - m.heat_exchanger_outlet_temperature_cold_stream
#     if dTa != dTb:
#         LMTD = (dTa-dTb) / np.log(dTa / dTb)
#     else:
#         LMTD = dTa
#     assert abs(LMTD - m.logarithmic_mean_temperature_difference) < 10e-1

    # m.heat_load = 110  # admixer
    # m.heat_exchanger_temperature_calculation(mixer_side='cold')
    # m.heat_load = 90  # bypass
    # m.heat_load = 110  # admixer
