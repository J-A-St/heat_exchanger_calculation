import math

from heat_exchanger import HeatExchanger


class TestHeatExchanger:
    """Unit tests for heat exchanger calculation"""

    def setup_model(self):
        """Setup coefficients for testing the heat exchanger class"""
        self.inlet_temperatures = [80, 20]
        self.film_heat_transfer_coefficients = [1.5, 3]
        self.heat_capacity_flows = [15, 20]
        self.heat_load = 25
        self.heat_exchanger = HeatExchanger(
            self.inlet_temperatures, self.film_heat_transfer_coefficients, self.heat_capacity_flows, self.heat_load)

    def test_overall_heat_transfer_coefficient(self):
        self.setup_model()
        overall_heat_transfer_coefficient = 1 / \
            (1 / self.film_heat_transfer_coefficients[0] +
             1 / self.film_heat_transfer_coefficients[1])
        assert overall_heat_transfer_coefficient == self.heat_exchanger.overall_heat_transfer_coefficient

    def test_outlet_temperatures(self):
        self.setup_model()
        outlet_temperature_hot_stream = self.inlet_temperatures[0] - \
            self.heat_load / self.heat_capacity_flows[0]
        outlet_temperature_cold_stream = self.inlet_temperatures[1] + \
            self.heat_load / self.heat_capacity_flows[1]
        assert outlet_temperature_hot_stream == self.heat_exchanger.outlet_temperature_hot_stream
        assert outlet_temperature_cold_stream == self.heat_exchanger.outlet_temperature_cold_stream

    def test_logarithmic_temperature_difference(self):
        self.setup_model()
        temperature_difference_a = self.inlet_temperatures[0] - \
            self.heat_exchanger.outlet_temperature_cold_stream
        temperature_difference_b = self.heat_exchanger.outlet_temperature_hot_stream - \
            self.inlet_temperatures[1]
        if temperature_difference_a == temperature_difference_b:
            logarithmic_temperature_difference = temperature_difference_a
        else:
            logarithmic_temperature_difference = (
                temperature_difference_a - temperature_difference_b) / math.log(temperature_difference_a / temperature_difference_b)
        assert abs(logarithmic_temperature_difference -
                   self.heat_exchanger.logarithmic_temperature_difference) <= 10e-10

        self.heat_exchanger.heat_capacity_flow_hot_stream = 20
        self.heat_exchanger.heat_capacity_flow_cold_stream = 20

        assert self.heat_exchanger.logarithmic_temperature_difference == self.heat_exchanger.inlet_temperature_hot_stream - \
            self.heat_exchanger.outlet_temperature_cold_stream

    def test_area(self):
        self.setup_model()
        area = self.heat_load / (self.heat_exchanger.overall_heat_transfer_coefficient *
                                 self.heat_exchanger.logarithmic_temperature_difference)
        assert area == self.heat_exchanger.area


if __name__ == "__main__":
    TestHeatExchanger()
