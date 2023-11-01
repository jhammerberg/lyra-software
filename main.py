import numpy as np
import matplotlib.pyplot as plt

# Constants
rocket_mass = 0.194  # mass of the rocket with propellant mass (Kg)
burn_time = 1.60   # Duration of the D12-3 rocket engine burn in seconds
drag_coefficient = 0.75 # Drag coefficient of model rocket
parachute_area = .08 # Initial parachute area (m^2)- still needs measuring
parachute_deploy_time = 6.5 # Time when the parachute deploys in seconds
g = 9.81          # Acceleration due to gravity 

# Parameters for the graphs to come. Total fight time to be finalized after constants are firm
time_step = 0.01  # Time step for simulation (s)
total_time = 30 # Total simulation time (s)

# Arrays to store time, velocity, and altitude data
time_points = [0]
velocity_points = [0]
altitude_points = [0]

# Time and thrust data points based on the graph on Estes' website for D-12 engine. Could be expanded on as some data is missing
thrust_data = [(0.0, 0.0), (0.25, 25.0), (0.30, 32.90),(0.35, 20.00),(0.40, 15.90), (0.50, 10.0), (1.0, 9.8), (1.6, 0.0)] 

def thrust_profile(t): # Part of the extra requirements: calculates the thrust of the rocket based on the array info above so it changes based on time
    for i in range(len(thrust_data) - 1):
        if thrust_data[i][0] <= t < thrust_data[i + 1][0]:
            t1, thrust1 = thrust_data[i]
            t2, thrust2 = thrust_data[i + 1]
            # Linearly interpolate between data points
            return thrust1 + (thrust2 - thrust1) * (t - t1) / (t2 - t1)
    return 0.0  

# Base values of velocity, time and height
t = 0
v = 0
h = 0.05
parachute_deployed = False # will be true at when t >= parachute_deploy_time
rocket_area = 0.01  # Cross sectional area of the rocket, will be used until the parachute is deployed. still needs to be measured

max_altitude = 0 #used establish a value of when rocket is at max height, used later 
impact_time = None #used establish a value of when the rocket will hit the ground 

while t < total_time:
    # Calculate thrust at the current time based on thrust profile function above
    thrust = thrust_profile(t)
 
    drag = 0.5 * drag_coefficient * rocket_area * v * 2 * 1.22
    
    if t < burn_time: # This if function is not completely correct. I need a chart/graph of the mass change per time iteration. But for now mass change is instant
        net_force = thrust - rocket_mass * g - drag # During burn phase, update rocket mass and calculate net force with original weight
    else:
        # After burn time, update rocket mass to a lower value due to no more propellant
        rocket_mass = .175
        net_force = thrust - rocket_mass * g - drag  # Recalculate net force with updated weight


    acceleration = net_force / rocket_mass

    # Update velocity and altitude
    v += acceleration * time_step
    h += v * time_step

    # Update time
    t += time_step

    # Extra: Update rocket area based on parachute deployment
    if t >= parachute_deploy_time and not parachute_deployed:
        rocket_area = parachute_area
        g = 7 # Desired terminal velocity reached after parachute deploys, can/will be changed based on parachute area
        parachute_deployed = True
        
     # Track and establish max altitude and impact time
    if h > max_altitude:
        max_altitude = h
    if h <= 0 and impact_time is None:
        impact_time = t

    # Store data for plotting
    time_points.append(t)
    velocity_points.append(v)
    altitude_points.append(h)

# Graphs
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(time_points, velocity_points)
plt.title('Rocket Velocity vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

plt.subplot(2, 1, 2)
plt.plot(time_points, altitude_points)
plt.title('Rocket Altitude vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.tight_layout()
plt.show()

Round_max_altitude = round(max_altitude,2)
Round_impact_time = round(impact_time,2)
max_altitude_ft = round(Round_max_altitude * 3.281,2)

# Shell will display the maximum height the rocket will reach as well as the time at which it will impact the ground
print(f"Maximum Altitude: {Round_max_altitude} meters or {max_altitude_ft} feet") 
print(f"Time of Impact: {Round_impact_time} seconds")
