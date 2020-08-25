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

## Description HeatExchanger

Framework to calculate the outlet temperatures, the logarithmic temperature difference, the overall heat transfer coefficient and the needed area for a counter-current heat exchanger.

Input:
* Inlet temperatures (°C)
* Film heat transfer coefficients (kW/(m2K))
* Heat capacity flows = specific heat capacity * mass flow (kW/K)
* Heat load (kW)
* Mixer type hot side -- none, bypass, or admixer
* Mixer type cold side -- none, bypass, or admixer
* Mixer fraction hot side -- 0...1 ((kg/s)/(kg/s))
* Mixer fraction cold side -- 0...1 ((kg/s)/(kg/s))

Properties of heat exchanger:
* Inlet temperatures (°C)
* Film heat transfer coefficients (kW/(m2K))
* Heat capacity flows = specific heat capacity * mass flow (kW/K)
* Heat load (kW)
* Outlet temperatures (°C)
* Overall heat transfer coefficient (kW/(m2K))
* Logarithmic temperature difference (K)
* Area (m2)

## Description HeatExchangerReversed

Framework to calculate the inlet, outlet temperatures, needed mixer fraction to compensate too large or small area (different operating case) for a counter-current heat exchanger. The logarithmic mean temperature difference is reversed using the Lambert W-function, first mentioned by Euler (1779), as explained by Chen (2019).

Input:
* Inlet temperatures (°C)
* Film heat transfer coefficients (kW/(m2K))
* Heat capacity flows = specific heat capacity * mass flow (kW/K)
* Heat load (kW)
* Existent area (m2)

Properties of heat exchanger:
* Inlet temperatures (°C)
* Film heat transfer coefficients (kW/(m2K))
* Heat capacity flows = specific heat capacity * mass flow (kW/K)
* Heat load (kW)
* Outlet temperatures (°C)
* Overall heat transfer coefficient (kW/(m2K))
* Logarithmic temperature difference (K)
* Needed mixer type: none, bypass, or admixer
* Mixer fraction ((kg/s)/(kg/s))

Reference
* Chen, J.J.J.,2019. Logarithmic mean: Chen's approximation or explicit solution?. Computers and Chemical Engineering. 120,1-3.
* Euler, L.,1779. De serie Lambertine plurimisque eius insignibus proprietatibus. Acta Academiae scientiarum imperialis petropolitanae, 29-51.
