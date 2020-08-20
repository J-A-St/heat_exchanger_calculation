import numpy as np

from heat_exchanger import HeatExchanger

inlet_temperatures = [80.0, 20.0]
film_heat_transfer_coefficients = [1, 1]
heat_capacity_flows = [5, 2.5]
heat_load = 100
mixer_type_hot = 'none'
mixer_type_cold = 'none'
mixer_fraction_hot = 0
mixer_fraction_cold = 0


def setup_model():
    """Setup coefficients for testing the heat exchanger class"""
    return HeatExchanger(
        inlet_temperatures=inlet_temperatures,
        film_heat_transfer_coefficients=film_heat_transfer_coefficients,
        heat_capacity_flows=heat_capacity_flows,
        heat_load=heat_load,
        mixer_type_hot=mixer_type_hot,
        mixer_type_cold=mixer_type_cold,
        mixer_fraction_hot=mixer_fraction_hot,
        mixer_fraction_cold=mixer_fraction_cold)


def test_overall_heat_transfer_coefficient():
    m = setup_model()
    overall_heat_transfer_coefficient = 1 / \
        (1 / film_heat_transfer_coefficients[0] +
         1 / film_heat_transfer_coefficients[1])
    assert overall_heat_transfer_coefficient == m.overall_heat_transfer_coefficient


def test_outlet_temperatures():
    m = setup_model()
    outlet_temperature_hot_stream = inlet_temperatures[0] - \
        m.heat_load / heat_capacity_flows[0]
    outlet_temperature_cold_stream = inlet_temperatures[1] + \
        m.heat_load / heat_capacity_flows[1]
    assert outlet_temperature_hot_stream == m.outlet_temperature_hot_stream
    assert outlet_temperature_cold_stream == m.outlet_temperature_cold_stream


def test_logarithmic_temperature_difference_no_mixer():
    m = setup_model()
    temperature_difference_a = inlet_temperatures[0] - \
        m.outlet_temperature_cold_stream
    temperature_difference_b = m.outlet_temperature_hot_stream - \
        inlet_temperatures[1]
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10

    m.heat_capacity_flow_hot_stream = 20
    m.heat_capacity_flow_cold_stream = 20

    assert m.logarithmic_temperature_difference == m.inlet_temperature_hot_stream - \
        m.outlet_temperature_cold_stream


def test_area_no_mixer():
    m = setup_model()
    area = m.heat_load / (m.overall_heat_transfer_coefficient *
                          m.logarithmic_temperature_difference)
    assert area == m.area


def test_heat_exchanger_temperatures_bypass_hot_side():
    m = setup_model()
    m.mixer_type_hot = 'bypass'
    m.mixer_fraction_hot = 0.2
    assert m.heat_exchanger_inlet_temperature_hot_stream == inlet_temperatures[0]
    assert m.heat_exchanger_outlet_temperature_hot_stream == inlet_temperatures[0] - heat_load / (heat_capacity_flows[0] * (1 - m.mixer_fraction_hot))
    temperature_difference_a = (inlet_temperatures[0] - heat_load / (heat_capacity_flows[0] * (1 - m.mixer_fraction_hot))) - inlet_temperatures[1]
    temperature_difference_b = inlet_temperatures[0] - (inlet_temperatures[1] + heat_load / heat_capacity_flows[1])
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_bypass_cold_side():
    m = setup_model()
    m.mixer_type_cold = 'bypass'
    m.mixer_fraction_cold = 0.2
    assert m.heat_exchanger_inlet_temperature_cold_stream == inlet_temperatures[1]
    assert m.heat_exchanger_outlet_temperature_cold_stream == inlet_temperatures[1] + heat_load / (heat_capacity_flows[1] * (1 - m.mixer_fraction_cold))
    temperature_difference_a = (inlet_temperatures[0] - heat_load / heat_capacity_flows[0]) - inlet_temperatures[1]
    temperature_difference_b = inlet_temperatures[0] - (inlet_temperatures[1] + heat_load / (heat_capacity_flows[1] * (1 - m.mixer_fraction_cold)))
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_bypass_both_sides():
    m = setup_model()
    m.mixer_type_hot = 'bypass'
    m.mixer_fraction_hot = 0.2
    m.mixer_type_cold = 'bypass'
    m.mixer_fraction_cold = 0.2
    temperature_difference_a = (inlet_temperatures[0] - heat_load / (heat_capacity_flows[0] * (1 - m.mixer_fraction_hot))) - inlet_temperatures[1]
    temperature_difference_b = inlet_temperatures[0] - (inlet_temperatures[1] + heat_load / (heat_capacity_flows[1] * (1 - m.mixer_fraction_cold)))
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_admixer_hot_side():
    m = setup_model()
    m.mixer_type_hot = 'admixer'
    m.mixer_fraction_hot = 0.2
    assert m.heat_exchanger_inlet_temperature_hot_stream == (inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot)
    assert m.heat_exchanger_outlet_temperature_hot_stream == (inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot) - heat_load / (heat_capacity_flows[0] * (1 + m.mixer_fraction_hot))
    assert m.heat_exchanger_outlet_temperature_hot_stream == inlet_temperatures[0] - heat_load / heat_capacity_flows[0]
    temperature_difference_a = (inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot) - heat_load / (heat_capacity_flows[0] * (1 + m.mixer_fraction_hot)) - inlet_temperatures[1]
    temperature_difference_b = (inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot) - (inlet_temperatures[1] + heat_load / heat_capacity_flows[1])
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_admixer_cold_side():
    m = setup_model()
    m.mixer_type_cold = 'admixer'
    m.mixer_fraction_cold = 0.2
    assert m.heat_exchanger_inlet_temperature_cold_stream == (inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold)
    assert m.heat_exchanger_outlet_temperature_cold_stream == (inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold) + heat_load / (heat_capacity_flows[1] * (1 + m.mixer_fraction_cold))
    temperature_difference_a = (inlet_temperatures[0] - heat_load / heat_capacity_flows[0]) - (inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold)
    temperature_difference_b = inlet_temperatures[0] - ((inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold) + heat_load / (heat_capacity_flows[1] * (1 + m.mixer_fraction_cold)))
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_admixer_both_sides():
    m = setup_model()
    m.mixer_type_hot = 'admixer'
    m.mixer_fraction_hot = 0.2
    m.mixer_type_cold = 'admixer'
    m.mixer_fraction_cold = 0.2
    temperature_difference_a = ((inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot) - heat_load / (heat_capacity_flows[0] * (1 + m.mixer_fraction_hot))) - ((inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold))
    temperature_difference_b = ((inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot)) - ((inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold) + heat_load / (heat_capacity_flows[1] * (1 + m.mixer_fraction_cold)))
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_bypass_hot_side_admixer_cold_side():
    m = setup_model()
    m.mixer_type_hot = 'bypass'
    m.mixer_fraction_hot = 0.2
    m.mixer_type_cold = 'admixer'
    m.mixer_fraction_cold = 0.2
    temperature_difference_a = (inlet_temperatures[0] - heat_load / (heat_capacity_flows[0] * (1 - m.mixer_fraction_hot))) - ((inlet_temperatures[1] + m.outlet_temperature_cold_stream * m.mixer_fraction_cold) / (1 + m.mixer_fraction_cold))
    temperature_difference_b = inlet_temperatures[0] - (inlet_temperatures[1] + heat_load / heat_capacity_flows[1])
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10


def test_heat_exchanger_temperatures_admixer_hot_side_bypass_cold_side():
    m = setup_model()
    m.mixer_type_hot = 'admixer'
    m.mixer_fraction_hot = 0.2
    m.mixer_type_cold = 'bypass'
    m.mixer_fraction_cold = 0.2
    temperature_difference_a = (inlet_temperatures[0] - heat_load / heat_capacity_flows[0]) - inlet_temperatures[1]
    temperature_difference_b = ((inlet_temperatures[0] + m.outlet_temperature_hot_stream * m.mixer_fraction_hot) / (1 + m.mixer_fraction_hot)) - (inlet_temperatures[1] + heat_load / (heat_capacity_flows[1] * (1 - m.mixer_fraction_cold)))
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.logarithmic_temperature_difference) <= 10e-10
