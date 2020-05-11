
class HeatExchanger:
    """Class for heat exchanger calculation"""

    def __init__(self, film_heat_transfer_coefficient_hot_side, film_heat_transfer_coefficient_cold_side):

        self.film_heat_treansfer_coefficient_hot_stream = film_heat_transfer_coefficient_hot_side
        self.film_heat_treansfer_coefficient_cold_stream = film_heat_transfer_coefficient_cold_side

    @property
    def overall_heat_treansfer_coefficient(self):
        return 1 / (1 / self.film_heat_treansfer_coefficient_hot_stream + 1 / self.film_heat_treansfer_coefficient_cold_stream)

    def __repr__(self):
        pass

    def __str__(self):
        pass
