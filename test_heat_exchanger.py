from heat_exchanger import HeatExchanger


class TestHeatExchanger:
    """Unit tests for heat exchanger calculation"""

    def setup_model(self):
        """Setup coefficients for testing the heat exchanger class"""
        self.inlet_temperatures = [80, 20]
        self.film_heat_transfer_coefficients = [1500, 3000]
        self.heat_capacity_flows = [15, 20]
        self.heat_load = 25
        self.heat_exchanger = HeatExchanger(
            self.inlet_temperatures, self.film_heat_transfer_coefficients, self.heat_capacity_flows, self.heat_load)

    def test_overall_heat_transfer_coefficient(self):
        self.setup_model()
        overall_heat_transfer_coefficient = 1 / \
            (1 / self.film_heat_transfer_coefficients[0] +
             1 / self.film_heat_transfer_coefficients[1])
        assert overall_heat_transfer_coefficient == self.heat_exchanger.overall_heat_treansfer_coefficient

    def test_outlet_temperatures(self):
        self.setup_model()
        outlet_temperature_hot_stream = self.inlet_temperatures[0] - \
            self.heat_load / self.heat_capacity_flows[0]
        outlet_temperature_cold_stream = self.inlet_temperatures[1] + \
            self.heat_load / self.heat_capacity_flows[1]
        assert outlet_temperature_hot_stream == self.heat_exchanger.outlet_temperature_hot_stream
        assert outlet_temperature_cold_stream == self.heat_exchanger.outlet_temperature_cold_stream


if __name__ == "__main__":
    TestHeatExchanger()
