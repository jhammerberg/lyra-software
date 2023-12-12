# Lyra Software
Flight prediction software for team Lyra's Engineering 100 section 980 rocket.

## Simulation Features:
- Thrust Profile
- Mass Profile
- Parachute cross-sectional area 
- Drag Calculations
- Net force and Acceleration
- Velocity and Altitude prediction
- Max Altitude and impact time tracking

## How to use
### Required Packages:
- numpy
- matplotlib

Install command: `pip install numpy matplotlib`

Change `thrust_data` to the given data points of a particular engine.\
Change `parachute_deployment_time` to the time given by the rocket motor expected deployment time.\
Change `parachute_area` to the actual cross-sectional area of the parachute you're using.
Change `rocket_mass` for accurate acceleration simulations.
Adjust `time_step` to change the simulation's temporal resolution.
#
**Team:** Genevieve Rishikof, Abi Parivakkam, Jack Hammerberg, Mateo Castillo\
**Developer:** Mateo Castillo