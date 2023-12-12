import numpy as np
import matplotlib.pyplot as plt


# Constants
burn_time = 1.65  # Duration of the D12-5 rocket engine burn in seconds
drag_coefficient = 0.75 # Drag coefficient of model rocket
parachute_area = 0.168 # Initial parachute area (m^2)
parachute_deploy_time = 6.32 # Time when the parachute deploys in seconds
g = 9.81  # Acceleration due to gravity

time_step = 0.01  # Time step for simulation (s)
total_time = 60 # Total simulation time (s)

# Arrays to store time, velocity, altitude, acceleration, thrust, and mass change
time_points = [0]
velocity_points = [0]
altitude_points = [0]
acceleration_points = [0]
thrust_points = [0]
mass_points = [0]

# Time and thrust data points based on the graph on Estes' website for D-12 engine
thrust_data = [(0.0, 0.0), (0.049, 2.569), (0.116, 9.369),(0.184, 17.275),(0.237, 24.258), (0.282, 29.73), (0.297, 27.01), (0.311, 22.589),
               (0.322, 17.99), (0.348, 14.126), (0.386, 12.099), (0.442, 10.808), (0.546, 9.876), (0.718, 9.306), (0.879, 9.105), (1.066, 8.901), (1.257, 8.698),
                (1.436, 8.31), (1.59, 8.294), (1.612, 4.613), (1.65, 0)]

def thrust_profile(t): # Part of the extra requirements: calculates the thrust of the rocket based on the array info above so it changes based on time
    for i in range(len(thrust_data) - 1):
        if thrust_data[i][0] <= t < thrust_data[i + 1][0]:
            t1, thrust1 = thrust_data[i]
            t2, thrust2 = thrust_data[i + 1]
            # Linearly interpolate between data points
            return thrust1 + (thrust2 - thrust1) * (t - t1) / (t2 - t1)
    return 0.0

# Time and mass data points. Starts with wet mass and decreases to dry mass
mass_loss_data = [(0.0, 0.1900), (0.049, 0.1899), (0.116, 0.1894),(0.184, 0.1882),(0.237, 0.1869), (0.282, 0.1854), (0.297,0.1848), (0.311, 0.1844),
               (0.322, 0.1841), (0.348, 0.1836), (0.386, 0.1829), (0.442, 0.1821), (0.546, 0.1808), (0.718, 0.1787), (0.879, 0.1769), (1.066, 0.1748), (1.257, 0.1726),
                (1.436, 0.1707), (1.59, 0.1692), (1.612, 0.1690), (1.65, 0.1689)]

def mass_profile(t): # Assigns a mass to the rocket per timestamp based on mass_loss_data. after the list runs out, mass will be 0.1689 kg until the end
    for i in range(len(mass_loss_data) - 1):
        if mass_loss_data[i][0] <= t < mass_loss_data[i + 1][0]:
            m1, mass1 = mass_loss_data[i]
            m2, mass2 = mass_loss_data[i + 1]
            # Linearly interpolate between data points
            return mass1 + (mass2 - mass1) * (t - m1) / (m2 - m1)
    return 0.1689 # Mass of rocket after propellant runs out

# Base values of velocity, time and height
t = 0
v = 0
h = 0.05
parachute_deployed = False # will be true at when t >= parachute_deploy_time
rocket_area = 0.0017 # Cross sectional area of the rocket in m^2

max_altitude = 0 #used to establish a value of when rocket is at max height, used later 
impact_time = None #used to establish a value of when the rocket will hit the ground

while t < total_time:
    # Calculate thrust at the current time based on thrust profile function
    thrust = thrust_profile(t)
    # Calculate mass at the current time based on mass profile function
    rocket_mass = mass_profile(t)
   
    # Extra: Update rocket area based on parachute deployment
    if t >= parachute_deploy_time and not parachute_deployed:
        rocket_area = parachute_area
        parachute_deployed = True
    
 
    drag = 0.5 * drag_coefficient*1.22 * rocket_area * v*2
     
    net_force = thrust - (rocket_mass * g) - drag # During burn phase, update rocket mass and calculate net force

    acceleration = net_force / rocket_mass 

    # Update velocity and altitude
    v += acceleration * time_step
    h += v * time_step

    # Update time
    t += time_step

     # Track and establish max altitude and impact time
    if h > max_altitude:
        max_altitude = h
    if h <= 0 and impact_time is None:
        impact_time = t


    # Store data for plotting
    time_points.append(t)
    velocity_points.append(v)
    altitude_points.append(h)
    acceleration_points.append(acceleration)
    thrust_points.append(thrust)
    mass_points.append(rocket_mass)


# Graphs
plt.figure(figsize=(4,5))

plt.subplot(2, 1, 1)
plt.plot(time_points, velocity_points)
plt.title('Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

plt.subplot(2, 1, 2)
plt.plot(time_points, altitude_points)
plt.title('Rocket Altitude vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')

plt.tight_layout()
plt.show()

# Separate the velocity and altitude graphs from the rest

plt.figure(figsize=(4, 5))

plt.subplot(3, 1, 1)
plt.plot(time_points, acceleration_points)
plt.title('Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')

plt.subplot(3, 1, 2)
plt.plot(time_points, thrust_points)
plt.title('Thrust')
plt.xlabel('Time (s)')
plt.ylabel('Neutons (N)')

plt.subplot(3, 1, 3)
plt.plot(time_points, mass_points)
plt.title('Rocket mass change vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('mass (Kg)')

plt.tight_layout()
plt.show()

Round_max_altitude = round(max_altitude,2)
Round_impact_time = round(impact_time,2)
max_altitude_ft = round(Round_max_altitude * 3.281,2)

# Shell will display the maximum height the rocket will reach as well as the time at which it will impact the ground
print(f"Maximum Altitude: {Round_max_altitude} meters or {max_altitude_ft} feet") 
print(f"Time of Impact: {Round_impact_time} seconds")