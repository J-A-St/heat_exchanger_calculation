import math

from heat_exchanger import HeatExchanger


def setup_model():
    """Setup coefficients for testing the heat exchanger class"""
    return HeatExchanger(
        inlet_temperatures=[80, 20],
        film_heat_transfer_coefficients=[1.5, 3],
        heat_capacity_flows=[15, 20],
        heat_load=25)


def test_overall_heat_transfer_coefficient():
    m = setup_model()
    overall_heat_transfer_coefficient = 1 / \
        (1 / m.film_heat_transfer_coefficients[0] +
         1 / m.film_heat_transfer_coefficients[1])
    assert overall_heat_transfer_coefficient == m.heat_exchanger.overall_heat_transfer_coefficient


def test_outlet_temperatures():
    m = setup_model()
    outlet_temperature_hot_stream = m.inlet_temperatures[0] - \
        m.heat_load / m.heat_capacity_flows[0]
    outlet_temperature_cold_stream = m.inlet_temperatures[1] + \
        m.heat_load / m.heat_capacity_flows[1]
    assert outlet_temperature_hot_stream == m.heat_exchanger.outlet_temperature_hot_stream
    assert outlet_temperature_cold_stream == m.heat_exchanger.outlet_temperature_cold_stream


def test_logarithmic_temperature_difference():
    m = setup_model()
    temperature_difference_a = m.inlet_temperatures[0] - \
        m.heat_exchanger.outlet_temperature_cold_stream
    temperature_difference_b = m.heat_exchanger.outlet_temperature_hot_stream - \
        m.inlet_temperatures[1]
    if temperature_difference_a == temperature_difference_b:
        logarithmic_temperature_difference = temperature_difference_a
    else:
        logarithmic_temperature_difference = (
            temperature_difference_a - temperature_difference_b) / math.log(temperature_difference_a / temperature_difference_b)
    assert abs(logarithmic_temperature_difference -
               m.heat_exchanger.logarithmic_temperature_difference) <= 10e-10

    m.heat_exchanger.heat_capacity_flow_hot_stream = 20
    m.heat_exchanger.heat_capacity_flow_cold_stream = 20

    assert m.heat_exchanger.logarithmic_temperature_difference == m.heat_exchanger.inlet_temperature_hot_stream - \
        m.heat_exchanger.outlet_temperature_cold_stream


def test_area():
    m = setup_model()
    area = m.heat_load / (m.heat_exchanger.overall_heat_transfer_coefficient *
                          m.heat_exchanger.logarithmic_temperature_difference)
    assert area == m.heat_exchanger.area
