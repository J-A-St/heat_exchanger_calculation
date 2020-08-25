import numpy as np


class HeatExchanger:
    """Class for heat exchanger calculation

        Arguments:
            inlet_temperatures {float} -- List of inlet temperatures (°C) with hot stream [0] and cold stream [1]
            film_heat_transfer_coefficients {float} -- List of film heat transfer coefficients(kW/(m2K) with hot stream [0] and cold stream [1]
            heat_capacity_flows {float} -- List of heat capacity flows (kW/K) with hot stream [0] and cold stream [1]
            heat_load {float} -- Heat load (kW)
            mixer_type_hot {string} -- none, bypass, or admixer
            mixer_type_cold {string} -- none, bypass, or admixer
            mixer_fraction_hot {float} -- 0...1 ((kg/s)/(kg/s))
            mixer_fraction_cold {float} -- 0...1 ((kg/s)/(kg/s))
        Properties:
            inlet_temperature_hot_stream {float} -- inlet temperature hot stream (°C)
            inlet_temperature_cold_stream {float} -- inlet temperature cold stream (°C)
            heat_exchanger_inlet_temperature_hot_stream {float} -- inlet temperature hot stream in mixer (°C)
            heat_exchanger_inlet_temperature_cold_stream {float} -- inlet temperature cold stream in mixer (°C)
            film_heat_transfer_coefficient_hot_stream {float} -- Film heat transfer coefficient hot stream (kW/(m2K))
            film_heat_transfer_coefficient_cold_stream {float} -- Film heat transfer coefficient cold stream (kW/(m2K))
            heat_capacity_flow_hot_stream {float} -- Heat capacity flow hot stream (kW/K)
            heat_capacity_flow_cold_stream {float} -- Heat capacity flow cold stream (kW/K)
            heat_load {float} -- Heat load (kW)
            overall_heat_transfer_coefficient {float} -- Resulting overall heat transfer coefficient (kW/(m2K))
            outlet_temperature_hot_stream {float} -- Resulting outlet temperature of hot stream (°C)
            outlet_temperature_cold_stream {float} -- Resulting outlet temperature of hot stream (°C)
            heat_exchanger_outlet_temperature_hot_stream {float} -- Resulting temperature hot stream out of mixer (°C)
            heat_exchanger_outlet_temperature_cold_stream {float} -- Resulting temperature cold stream out of mixer (°C)
            logarithmic_temperature_difference {float} -- Resulting logarithmic temperature difference (K)
            area {float} -- Resulting area (m2)
        """

    def __init__(self, inlet_temperatures, film_heat_transfer_coefficients, heat_capacity_flows, heat_load, mixer_type_hot='none', mixer_type_cold='none', mixer_fraction_hot=0, mixer_fraction_cold=0):
        self.mixer_type_hot = mixer_type_hot
        self.mixer_type_cold = mixer_type_cold
        self.mixer_fraction_hot = mixer_fraction_hot
        self.mixer_fraction_cold = mixer_fraction_cold
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
    def heat_exchanger_inlet_temperature_hot_stream(self):
        return self.heat_exchanger_inlet_temperature_calculation(self.inlet_temperature_hot_stream, self.heat_capacity_flow_hot_stream, self.mixer_type_hot, self.mixer_fraction_hot, 'hot')

    @property
    def heat_exchanger_inlet_temperature_cold_stream(self):
        return self.heat_exchanger_inlet_temperature_calculation(self.inlet_temperature_cold_stream, self.heat_capacity_flow_cold_stream, self.mixer_type_cold, self.mixer_fraction_cold, 'cold')

    @property
    def heat_exchanger_outlet_temperature_hot_stream(self):
        return self.heat_exchanger_outlet_temperature_calculation(self.heat_exchanger_inlet_temperature_hot_stream, self.heat_capacity_flow_hot_stream, self.mixer_type_hot, self.mixer_fraction_hot, 'hot')

    @property
    def heat_exchanger_outlet_temperature_cold_stream(self):
        return self.heat_exchanger_outlet_temperature_calculation(self.heat_exchanger_inlet_temperature_cold_stream, self.heat_capacity_flow_cold_stream, self.mixer_type_cold, self.mixer_fraction_cold, 'cold')

    @property
    def outlet_temperature_hot_stream(self):
        return self.inlet_temperature_hot_stream + self.stream_temperature_difference(self.heat_capacity_flow_hot_stream, 'none', 0, 'hot')

    @property
    def outlet_temperature_cold_stream(self):
        return self.inlet_temperature_cold_stream + self.stream_temperature_difference(self.heat_capacity_flow_cold_stream, 'none', 0, 'cold')

    @property
    def logarithmic_temperature_difference(self):
        temperature_difference_a = self.heat_exchanger_outlet_temperature_hot_stream - self.heat_exchanger_inlet_temperature_cold_stream
        temperature_difference_b = self.heat_exchanger_inlet_temperature_hot_stream - self.heat_exchanger_outlet_temperature_cold_stream
        if temperature_difference_a == temperature_difference_b:
            return temperature_difference_a
        else:
            return (temperature_difference_a - temperature_difference_b) / np.log(temperature_difference_a / temperature_difference_b)

    @property
    def area(self):
        return self.heat_load / (self.overall_heat_transfer_coefficient * self.logarithmic_temperature_difference)

    def heat_exchanger_inlet_temperature_calculation(self, inlet_temperature, heat_capacity_flow, mixer_type, mixer_fraction, stream_type):
        if mixer_type == 'bypass' or mixer_type == 'none':
            return inlet_temperature

        elif mixer_type == 'admixer':
            return (inlet_temperature + (inlet_temperature + self.stream_temperature_difference(heat_capacity_flow, 'none', 0, stream_type)) * mixer_fraction) / (1 + mixer_fraction)

        else:
            raise Exception("Sorry, you've misspelled the mixer type")

    def heat_exchanger_outlet_temperature_calculation(self, heat_exchanger_inlet_temperature, heat_capacity_flow, mixer_type, mixer_fraction, stream_type):
        return heat_exchanger_inlet_temperature + self.stream_temperature_difference(heat_capacity_flow, mixer_type, mixer_fraction, stream_type)

    def stream_temperature_difference(self, heat_capacity_flow, mixer_type, mixer_fraction, stream_type):
        if stream_type == 'hot':
            stream_type_sign = -1
        elif stream_type == 'cold':
            stream_type_sign = 1
        else:
            raise Exception("Sorry,you've misspelled the stream type")

        if mixer_type == 'bypass':
            return stream_type_sign * self.heat_load / (heat_capacity_flow * (1 - mixer_fraction))
        elif mixer_type == 'admixer':
            return stream_type_sign * self.heat_load / (heat_capacity_flow * (1 + mixer_fraction))
        elif mixer_type == 'none':
            return stream_type_sign * self.heat_load / heat_capacity_flow
        else:
            raise Exception("Sorry, you've misspelled the mixer type")

    def __repr__(self):
        pass

    def __str__(self):
        pass
