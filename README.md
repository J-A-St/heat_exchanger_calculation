# Heat exchanger calculation

Copyright 2020 Jan Stampfli

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

## Description

Framework to calculate the outlet temperatures, the logarithmic temperature difference, the overall heat transfer coefficient and the needed area for a counter-current heat exchanger.
Input:
* Inlet temperatures (°C)
* Film heat transfer coefficients (kW/(m2K))
* Heat capacity flows = specific heat capacity * mass flow (kW/s)
* Heat load (kW)
Results:
* Outlet temperatures (°C)
* Overall heat transfer coefficient (kW/(m2K))
* Logarithmic temperature difference (K)
* Area (m2)
