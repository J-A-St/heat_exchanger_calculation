from heat_exchanger import HeatExchanger


class TestHeatExchanger:
    """Unit tests for heat exchanger calculation"""

    def test_overall_heat_transfer_coefficient(self):
        film_heat_transfer_coefficient_hot_stream, film_heat_transfer_coefficient_cold_stream = 1500, 3000
        overall_heat_transfer_coefficient = 1 / \
            (1 / film_heat_transfer_coefficient_hot_stream +
             1 / film_heat_transfer_coefficient_cold_stream)
        heat_exchanger = HeatExchanger(
            film_heat_transfer_coefficient_hot_stream, film_heat_transfer_coefficient_cold_stream)
        assert overall_heat_transfer_coefficient == heat_exchanger.overall_heat_treansfer_coefficient


if __name__ == "__main__":
    TestHeatExchanger()
