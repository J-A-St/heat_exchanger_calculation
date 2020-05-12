import math


class HeatExchanger:
    """Class for heat exchanger calculation

        Arguments:
            inlet_temperatures {float} -- List of inlet temperatures (°C) with hot stream [0] and cold stream [1] 
            film_heat_transfer_coefficients {float} -- List of film heat transfer coefficients(kW/(m2K) with hot stream [0] and cold stream [1]
            heat_capacity_flows {float} -- List of heat capacity flows (kW/K) with hot stream [0] and cold stream [1]
            heat_load {float} -- Heat load (kW)
        Properties:
            inlet_temperature_hot_stream {float} -- inlet temperature hot stream (°C)
            inlet_temperature_cold_stream {float} -- inlet temperature cold stream (°C)
            film_heat_transfer_coefficient_hot_stream {float} -- Film heat transfer coefficient hot stream (kW/(m2K))
            film_heat_transfer_coefficient_cold_stream {float} -- Film heat transfer coefficient cold stream (kW/(m2K))
            heat_capacity_flow_hot_stream {float} -- Heat capacity flow hot stream (kW/K)
            heat_capacity_flow_cold_stream {float} -- Heat capacity flow cold stream (kW/K)
            heat_load {float} -- Heat load (kW)
            overall_heat_transfer_coefficient {float} -- Resulting overall heat transfer coefficient (kW/(m2K))
            outlet_temperature_hot_stream {float} -- Resulting outlet temperature of hot stream (°C)
            outlet_temperature_cold_stream {float} -- Resulting outlet temperature of hot stream (°C)
            logarithmic_temperature_difference {float} -- Resulting logarithmic temperature difference (K)
            area {float} --Resulting area (m2)
        """

    def __init__(self, inlet_temperatures, film_heat_transfer_coefficients, heat_capacity_flows, heat_load):
        self.inlet_temperature_hot_stream = inlet_temperatures[0]
        self.inlet_temperature_cold_stream = inlet_temperatures[1]
        self.film_heat_transfer_coefficient_hot_stream = film_heat_transfer_coefficients[0]
        self.film_heat_transfer_coefficient_cold_stream = film_heat_transfer_coefficients[1]
        self.heat_capacity_flow_hot_stream = heat_capacity_flows[0]
        self.heat_capacity_flow_cold_stream = heat_capacity_flows[1]
        self.heat_load = heat_load

    @property
    def overall_heat_transfer_coefficient(self):
        return 1 / (1 / self.film_heat_transfer_coefficient_hot_stream + 1 / self.film_heat_transfer_coefficient_cold_stream)

    @property
    def outlet_temperature_hot_stream(self):
        return self.inlet_temperature_hot_stream - self.stream_temperature_difference(self.heat_capacity_flow_hot_stream)

    @property
    def outlet_temperature_cold_stream(self):
        return self.inlet_temperature_cold_stream + self.stream_temperature_difference(self.heat_capacity_flow_cold_stream)

    @property
    def logarithmic_temperature_difference(self):
        temperature_difference_a = self.outlet_temperature_hot_stream - self.inlet_temperature_cold_stream
        temperature_difference_b = self.inlet_temperature_hot_stream - self.outlet_temperature_cold_stream
        if temperature_difference_a == temperature_difference_b:
            return temperature_difference_a
        else:
            return (temperature_difference_a - temperature_difference_b) / math.log(temperature_difference_a / temperature_difference_b)

    @property
    def area(self):
        return self.heat_load / (self.overall_heat_transfer_coefficient * self.logarithmic_temperature_difference)

    def stream_temperature_difference(self, heat_capacity_flow):
        return self.heat_load / heat_capacity_flow

    def __repr__(self):
        pass

    def __str__(self):
        pass
