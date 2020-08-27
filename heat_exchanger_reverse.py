import numpy as np
from scipy.special import lambertw


class HeatExchangerReverse():
    """Class for heat reversed exchanger calculation

        Arguments:
            inlet_temperatures {float} -- List of inlet temperatures (°C) with hot stream [0] and cold stream [1]
            film_heat_transfer_coefficients {float} -- List of film heat transfer coefficients(kW/(m2K) with hot stream [0] and cold stream [1]
            heat_capacity_flows {float} -- List of heat capacity flows (kW/K) with hot stream [0] and cold stream [1]
            heat_load {float} -- Heat load (kW)
            existent_area {float} -- Area of HEX (m2)
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
            area no mixer {float} -- Resulting area assuming no mixer (m2)
            mixer_type {string} -- Needed mixer type: none, bypass, or admixer
            admixer_fraction {float} -- 0...1 ((kg/s)/(kg/s))
            bypass_fraction {float} -- 0...1 ((kg/s)/(kg/s))
        """

    def __init__(self, inlet_temperatures, film_heat_transfer_coefficients, heat_capacity_flows, heat_load, existent_area):
        self.inlet_temperature_hot_stream = inlet_temperatures[0]
        self.inlet_temperature_cold_stream = inlet_temperatures[1]
        self.film_heat_transfer_coefficient_hot_stream = film_heat_transfer_coefficients[0]
        self.film_heat_transfer_coefficient_cold_stream = film_heat_transfer_coefficients[1]
        self.heat_capacity_flow_hot_stream = heat_capacity_flows[0]
        self.heat_capacity_flow_cold_stream = heat_capacity_flows[1]
        self.heat_load = heat_load
        self.existent_area = existent_area
        self.heat_exchanger_inlet_temperature_hot_stream = None
        self.heat_exchanger_outlet_temperature_hot_stream = None
        self.heat_exchanger_inlet_temperature_cold_stream = None
        self.heat_exchanger_outlet_temperature_cold_stream = None
        self.admixer_fraction = None
        self.bypass_fraction = None

    @property
    def overall_heat_transfer_coefficient(self):
        return 1 / (1 / self.film_heat_transfer_coefficient_hot_stream + 1 / self.film_heat_transfer_coefficient_cold_stream)

    @property
    def outlet_temperature_hot_stream(self):
        return self.inlet_temperature_hot_stream - self.heat_load / self.heat_capacity_flow_hot_stream

    @property
    def outlet_temperature_cold_stream(self):
        return self.inlet_temperature_cold_stream + self.heat_load / self.heat_capacity_flow_cold_stream

    @property
    def area_no_mixer(self):
        dTa = self.outlet_temperature_hot_stream - self.inlet_temperature_cold_stream
        dTb = self.inlet_temperature_hot_stream - self.outlet_temperature_cold_stream
        if dTa != dTb:
            logarithmic_mean_temperature_difference = (dTa - dTb) / np.log(dTa/dTb)
        else:
            logarithmic_mean_temperature_difference = dTa
        return self.heat_load / (self.overall_heat_transfer_coefficient * logarithmic_mean_temperature_difference)

    @property
    def mixer_type(self):
        if self.area_no_mixer > self.existent_area:
            # Not enough existing area: add admixer
            return 'admixer'
        elif self.area_no_mixer < self.existent_area:
            # Too much existing area: add bypass
            return 'bypass'
        else:
            # Correct existing area: no mixer
            return 'none'

    @property
    def logarithmic_mean_temperature_difference(self):
        return self.heat_load / (self.overall_heat_transfer_coefficient * self.existent_area)

    def heat_exchanger_temperature_calculation(self, mixer_side='none'):
        """Calculates inlet and outlet temperatures of the heat exchanger with wrong area (compensation using bypass or admixer)

        Args:
            mixer_side (str, optional): Indicates the side of the heat exchanger on which the mixer is incorporated. Defaults to 'none'.
        """
        if self.mixer_type == 'admixer':
            if mixer_side == 'hot':
                self.heat_exchanger_outlet_temperature_hot_stream = self.outlet_temperature_hot_stream
                self.heat_exchanger_inlet_temperature_cold_stream = self.inlet_temperature_cold_stream
                self.heat_exchanger_outlet_temperature_cold_stream = self.outlet_temperature_cold_stream

                dT_1 = self.heat_exchanger_outlet_temperature_hot_stream - self.heat_exchanger_inlet_temperature_cold_stream
                if dT_1 != self.logarithmic_mean_temperature_difference:
                    dT_LMTD = dT_1 / self.logarithmic_mean_temperature_difference
                    beta = - lambertw(-dT_LMTD * np.exp(-dT_LMTD), -1).real * 1 / dT_LMTD
                    dT_2 = beta * dT_1
                else:
                    dT_2 = dT_1
                self.heat_exchanger_inlet_temperature_hot_stream = self.heat_exchanger_inlet_temperature_cold_stream + dT_2
                self.admixer_fraction = (self.inlet_temperature_hot_stream - self.heat_exchanger_inlet_temperature_hot_stream) / (self.heat_exchanger_inlet_temperature_hot_stream - self.outlet_temperature_hot_stream)

            else:
                self.heat_exchanger_inlet_temperature_hot_stream = self.inlet_temperature_hot_stream
                self.heat_exchanger_outlet_temperature_hot_stream = self.outlet_temperature_hot_stream
                self.heat_exchanger_outlet_temperature_cold_stream = self.outlet_temperature_cold_stream

                dT_2 = self.heat_exchanger_inlet_temperature_hot_stream - self.heat_exchanger_outlet_temperature_cold_stream
                if dT_2 != self.logarithmic_mean_temperature_difference:
                    dT_LMTD = dT_2 / self.logarithmic_mean_temperature_difference
                    beta = - lambertw(-dT_LMTD * np.exp(-dT_LMTD), -1).real * 1 / dT_LMTD
                    dT_1 = beta * dT_2

                else:
                    dT_1 = dT_2
                self.heat_exchanger_inlet_temperature_cold_stream = self.heat_exchanger_outlet_temperature_hot_stream - dT_1
                self.admixer_fraction = (self.inlet_temperature_cold_stream - self.heat_exchanger_inlet_temperature_cold_stream) / (self.heat_exchanger_inlet_temperature_cold_stream - self.outlet_temperature_cold_stream)

        elif self.mixer_type == 'bypass':
            if mixer_side == 'hot':
                self.heat_exchanger_inlet_temperature_hot_stream = self.inlet_temperature_hot_stream
                self.heat_exchanger_inlet_temperature_cold_stream = self.inlet_temperature_cold_stream
                self.heat_exchanger_outlet_temperature_cold_stream = self.outlet_temperature_cold_stream

                dT_2 = self.heat_exchanger_inlet_temperature_hot_stream - self.heat_exchanger_outlet_temperature_cold_stream
                if dT_2 != self.logarithmic_mean_temperature_difference:
                    dT_LMTD = dT_2 / self.logarithmic_mean_temperature_difference
                    beta = - lambertw(-dT_LMTD * np.exp(-dT_LMTD), -1).real * 1 / dT_LMTD
                    dT_1 = beta * dT_2

                else:
                    dT_1 = dT_2
                self.heat_exchanger_outlet_temperature_hot_stream = self.heat_exchanger_inlet_temperature_cold_stream + dT_1
                self.bypass_fraction = (self.outlet_temperature_hot_stream - self.inlet_temperature_hot_stream) / (self.heat_exchanger_outlet_temperature_hot_stream - self.inlet_temperature_hot_stream)

            else:
                self.heat_exchanger_inlet_temperature_hot_stream = self.inlet_temperature_hot_stream
                self.heat_exchanger_outlet_temperature_hot_stream = self.outlet_temperature_hot_stream
                self.heat_exchanger_inlet_temperature_cold_stream = self.inlet_temperature_cold_stream

                dT_1 = self.heat_exchanger_outlet_temperature_hot_stream - self.heat_exchanger_inlet_temperature_cold_stream
                if dT_1 != self.logarithmic_mean_temperature_difference:
                    dT_LMTD = dT_1 / self.logarithmic_mean_temperature_difference
                    beta = - lambertw(-dT_LMTD * np.exp(-dT_LMTD), -1).real * 1 / dT_LMTD
                    dT_2 = beta * dT_1
                else:
                    dT_2 = dT_1
                self.heat_exchanger_outlet_temperature_cold_stream = self.heat_exchanger_inlet_temperature_hot_stream - dT_2
                self.bypass_fraction = (self.outlet_temperature_cold_stream - self.inlet_temperature_cold_stream) / (self.heat_exchanger_outlet_temperature_cold_stream - self.inlet_temperature_cold_stream)
        else:
            self.heat_exchanger_inlet_temperature_hot_stream = self.inlet_temperature_hot_stream
            self.heat_exchanger_outlet_temperature_hot_stream = self.outlet_temperature_hot_stream
            self.heat_exchanger_inlet_temperature_cold_stream = self.inlet_temperature_cold_stream
            self.heat_exchanger_outlet_temperature_cold_stream = self.outlet_temperature_cold_stream

    def __repr__(self):
        pass

    def __str__(self):
        pass
