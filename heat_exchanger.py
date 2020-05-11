
class HeatExchanger:
    """Class for heat exchanger calculation. First index of list is hot stream, and second index is cold stream. The following units are used:
        [temperatures] = K
        [film_heat_transfer_coefficients] = kW/(m2K)
        [heat_capacity_flows = specific_heat_transfer_coefficient * mass_flow] = kW/s 
        [heat_load] = kW"""

    def __init__(self, inlet_temperatures, film_heat_transfer_coefficients, heat_capacity_flows, heat_load):
        self.inlet_temperature_hot_stream = inlet_temperatures[0]
        self.inlet_temperature_cold_stream = inlet_temperatures[1]
        self.film_heat_treansfer_coefficient_hot_stream = film_heat_transfer_coefficients[0]
        self.film_heat_treansfer_coefficient_cold_stream = film_heat_transfer_coefficients[1]
        self.heat_capacity_flow_hot_stream = heat_capacity_flows[0]
        self.heat_capacity_flow_cold_stream = heat_capacity_flows[1]
        self.heat_load = heat_load

    @property
    def overall_heat_treansfer_coefficient(self):
        return 1 / (1 / self.film_heat_treansfer_coefficient_hot_stream + 1 / self.film_heat_treansfer_coefficient_cold_stream)

    @property
    def outlet_temperature_hot_stream(self):
        return self.inlet_temperature_hot_stream - self.stream_temperature_difference(self.heat_capacity_flow_hot_stream)

    @property
    def outlet_temperature_cold_stream(self):
        return self.inlet_temperature_cold_stream + self.stream_temperature_difference(self.heat_capacity_flow_cold_stream)

    def stream_temperature_difference(self, heat_capacity_flow):
        return self.heat_load / heat_capacity_flow

    def __repr__(self):
        pass

    def __str__(self):
        pass
